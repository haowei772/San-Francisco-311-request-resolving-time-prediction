import pandas as pd
import numpy as np

def import_data(filepath):
    '''
    Import the data from a csv file into a pandas dataframe and
    parse desired columns to datetime
    INPUT: filepath - a filepath in string
    OUTPUT: a dataframe
    '''
    df = pd.read_csv(filepath)

    df = df.sort_values('CaseID')
    df.set_index('CaseID', inplace = True)

    ''' parse columns to datetime'''
    dt_list = ['Opened','Closed','Updated'] # list of datetime columns
    time_format = '%m/%d/%Y %I:%M:%S %p'
    dft = parsedate(df, dt_list, time_format) # parse ['Opened','Closed','Updated'] to datetime
    return dft

def clean_data(dft):
    '''
    Clean data by removing cases that are not closed, closed before opened, or duplictaed.
    Write the clean dataframe to a scv file.
    INPUT: dft - a pandas dataframe, folder - a string of output loction
    OUTPUT: a dataframe
    '''
    ''' remove cases that are not closed'''
    condition = dft['Closed'].notnull()
    dft_closed = dft[condition] # cases that are closed

    '''calculate the process time in days and hours'''
    dft_closed['Process_days'] = dft_closed['Closed'] - dft_closed['Opened']
    dft_closed['Process_hours'] = dft_closed['Process_days'].apply(days_to_hours)

    ''' only keep cases that are closed after opened '''
    dft_right_dates = dft_closed[dft_closed['Process_hours'] > 0]

    ''' remove duplicated cases '''
    dft_duplicates, dft_valid = check_word_in_col(dft_right_dates, 'Status Notes', 'Duplicate')

    '''convert Process_days to float'''
    dft_valid['Process_days'] = dft_valid['Process_hours']/24.0

    # '''save raw valid cases'''
    # filename_valid = 'SF311_valid_raw.csv'
    # dft_valid_csv_path = folder + filename_valid
    # dft_valid.to_csv(dft_valid_csv_path)

    '''remove unnecessary columns '''
    drop_col = ['Updated','Status', 'Media URL']
    dft_valid_reduced = dft_valid.drop(drop_col, axis =1)
    # filename_reduced = 'SF311_valid_reduced.csv'
    # dft_valid_reduced_csv_path = folder + filename_reduced
    # dft_valid_reduced.to_csv(dft_valid_reduced_csv_path)
    return dft_valid_reduced

def check_word_in_col(df, column, word='Duplicate'):
    '''
    Check if a specific word (e.g.,'Duplicate') is in the column of an entry, returns a dataframe
    that contains the entries with the word.
    INPUT: df - a pandas dataframe, column - string of the column name, word - string of a specific word
    OUTPUT: a dataframe that contains the entries with the word
    '''
    df1 = df.copy()
    get_str_list = lambda x: str(x).split() # convert a string to a list of string
    check_dup = lambda x: word in x

    df1[column+'1'] = df1[column].apply(get_str_list) # turn df1[column] into a list of strings
    cond = df1[column+'1'].apply(check_dup) # check if df1[column+'1'] contains the word
    return df[cond]

def parsedate(df, columns, time_format):
    '''
    Parse the designated columns to datetime according to the input format
    INPUT: df - a pandas dataframe, columns - list of the columns name,
    time_format - string of a time format
    OUTPUT: a dataframe
    '''
    for column in columns:
        df[column] = pd.to_datetime(df[column], format = time_format)
    return df

def days_to_hours(dt):
    '''
    Convert days to hours
    INPUT: dt - a pandas datetime.timedelta object
    OUTPUT: number of hours in float
    '''
    hours = dt.total_seconds()/3600#(td.seconds//60)%60
    return np.round(hours,1)

def add_features(df):
    '''
    Add new features to the dataframe, including Day of week, Month, Year, Weekend, Holiday
    INPUT: df - a dataframe
    OUTPUT: a dataframe with added columns
    '''
    df1 = df.copy()

    '''Add features: Day of week, Month, Year, Weekend '''
    df1['Day_Of_Week'] = df1['Opened'].dt.dayofweek
    df1['Month'] = df1['Opened'].dt.month
    df1['Year'] = df1['Opened'].dt.year

    df1['Weekend'] = (df1['Day_Of_Week'].isin((5,6))).astype(int) # if the open day is at weekend
    '''Add feature Holiday and Before_Holiday'''
    df1['Opened_Int'] = df1['Opened'].astype(np.int64)

    cal = calendar()
    holidays = cal.holidays()
    df1['Holiday'] = ((df1['Opened'].dt.date).astype('datetime64').isin(holidays)).astype(int)
    df1['Before_Holiday'] = (((df1['Opened'].dt.date).astype('datetime64')+timedelta(days = 1))\
                             .isin(holidays)).astype(int)
    num_of_holiday = len(df1[df1['Holiday'] == 1])
    num_of_before_holiday = len(df1[df1['Before_Holiday'] == 1])

    df1['Open_Time'] = df1['Opened'].astype(int).astype(float)/(10**16)
    df1['Request Topic'] = df1['Request Type']
    return df1

if __name__ == '__main__':
    '''Read data from csv file'''
    filepath = '../data/SF311.csv'
    dft = import_data(filepath)

    '''Clean the dataset, and save to a csv file'''
    dft_clean = clean_data(dft)
    filename_clean = 'SF311_clean.csv'
    dft_clean.to_csv(folder+filename_engineered)
