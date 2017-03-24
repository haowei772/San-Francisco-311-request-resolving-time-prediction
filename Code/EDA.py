import pandas as pd
import numpy as np
from collections import defaultdict
import matplotlib.pyplot as plt
import seaborn as sns

from pandas.tseries.holiday import USFederalHolidayCalendar as calendar
from datetime import date, datetime, time, timedelta
from scipy import stats

sns.set()

def general_explore_file(filepath, show = False):
    df = pd.read_csv(filepath)
    if show:
        explore_df(df)
    return df

def get_prep_data(filepath, parse_dt = ['Opened', 'Closed'], fix_index = 'CaseID'):
    df = pd.read_csv(filepath, parse_dates =parse_dt, infer_datetime_format=True)
    if fix_index:
        df.set_index(fix_index, inplace = True)
    return df

def read_csv_chunks_into_df(file_path, chunk_size, parse_date=False):
    if parse_date:
        chunks = pd.read_csv(file_path, parse_dates= ['Opened','Closed','Updated'], infer_datetime_format=True, chunksize = chunk_size )
    else:
        chunks = pd.read_csv(file_path, chunksize = chunk_size )
    df = pd.concat(chunks)
    return df

def explore_df(df):
    print '*********** Shape of df **************'
    print df.shape
    features = df.columns.values
    print '********** Number of features ***************'
    print len(features)
    print '********** Features ***************'
    print features
    print '******* Head of df ******************'
    print df.head()
    print '******* Info of df ******************'
    print df.info()
    print '******** Description of df *****************'
    print df.describe()
    return

def import_data(folder, filename):
    '''import the data and set the right datetime '''
    folder = folder
    filename_original = filename
    filepath = folder + filename_original
    df = general_explore_file(filepath)

    df = df.sort_values('CaseID')
    df.set_index('CaseID', inplace = True)

    ''' parse dates'''
    dt_list = ['Opened','Closed','Updated'] # list of datetime columns
    time_format = '%m/%d/%Y %I:%M:%S %p'
    dft = parsedate(df, dt_list, time_format) # parse ['Opened','Closed','Updated'] to timedate
    return dft

def get_unique(df):
    features = df.columns.values
    print '********* Number of unique values **********'
    for feature in features:
        print feature,' ', len(df[feature].unique())
    return

def get_missing(df):
    print '********* Number of missing values **********'
    df2 = df.isnull()
    features = df.columns.values
    for feature in features:
        temp = df[df2[feature]]
        print feature,' ', len(temp)

def drop_na_row(df,feature):
    df = df.ix[df[feature].notnull(), :]
    return df

def get_value_counts(df, feature_list):
    for feature in feature_list:
        print '************ '+feature+' value counts ***********'
        print df[feature].value_counts(dropna = False)
    return

def parsedate(df, columns, time_format):
    for column in columns:
        df[column] = pd.to_datetime(df[column], format = time_format)
    return df

def days_to_minutes(dt):
    return  dt.total_seconds()//60#(td.seconds//60)%60

def days_to_hours(dt):
    hours = dt.total_seconds()/3600#(td.seconds//60)%60
    return np.round(hours,1)

def get_sorted_category_value(df, category):
    ''' returns sorted categorical values based on the mean process_hours '''
    dfm = df.groupby(category).mean()
    dfm = dfm.sort_values('Process_hours')
    return dfm.index

def category_to_numer_dict(df, category, values):
    '''
    Change a categorical column to numeric and save the categorical values in a
    dictionary for later reference values is sorted list of categorical values
    '''
    dict = defaultdict(str)
    for i,value in enumerate(values):
        dict[i] = value # store the categorical values in a dictionary for reference
        df.ix[df[category]==value, category] = i
    df[category].astype(int, inplace=True)
    return dict

def category_to_numer_basic(df, category):
    '''Change a categorical column to numeric and save the categorical
    values in a dictionary for later reference (basic version)'''
    values = df[category].unique()
    for i,value in enumerator(values):
        df.ix[df[category]==value, category] = i
    df[category].astype(int, inplace=True)
    return df

def batch_process_categories(df, categories):
    '''convert categorical features to numerical by batch,
    return a dictionary of dictionaries storing the mapping of categorical value to number'''
    cate_dict = {}
    for category in categories:
        '''Convert the categoricl column to numerical'''
        if  category in df.columns.values:
            cate_val = get_sorted_category_value(df,category)
            '''The category_to_numer_dict() modify the input dataframe by side-effect and return a dictionary'''
            cate_dict[category] = category_to_numer_dict(df, category, cate_val)
    return cate_dict

def check_group_mean(df, groupby_cols, target_cols):
    for col in groupby_cols:
        dfm = df.groupby(col).mean()
        print dfm[target_cols]
    return

def check_group_stats(df, groupby_cols, target_cols):
    for col in groupby_cols:
        dfm = df.groupby(col).describe()
        print dfm[target_cols]
    return

def plot_data_on_date(df, data_col, year = False, month = False, day = False, dot = True):
    ''' set index to date and plot df column data against the index, year can be Boolean or int'''
    dfcp = df.copy()
    dfcp.set_index('Opened', inplace = True)
    if (type(year)==int) & (type(month)==int) & (type(day)==int):
        cond1 = dfcp.index.year == year
        cond2 = dfcp.index.month == month
        cond3 = dfcp.index.day == day
        dfcp1 = dfcp[cond1 & cond2 & cond3]
    elif (type(year)==int) & (type(month)==int):
        cond1 = dfcp.index.year == year
        cond2 = dfcp.index.month == month
        dfcp1 = dfcp[cond1 & cond2]
    elif type(year)==int:
        dfcp1 = dfcp[dfcp.index.year == year]
    else:
        dfcp1 = dfcp
    if dot:
        dfcp1[data_col].plot(figsize=(18,16), c='m', alpha = 0.2,style='o')
    else:
        dfcp1[data_col].plot(figsize=(18,16), c='k', alpha = 0.2)
    plt.show()
    return

'''The following function is not necessary, becasue plot_data_on_date() can do scatter plot'''
'''plot a scatter plot on data'''
def scatter_data_on_date(df, data_col, year = False, month = False, day = False):
    ''' set index to date and plot df column data against the index; year, month, and day can be Boolean or int'''
    dfcp = df.copy()
    dfcp['Opened_Int'] = dfcp['Opened'].astype(np.int64)
    dfcp.set_index('Opened', inplace = True)
    if (type(year)==int) & (type(month)==int) & (type(day)==int):
        cond1 = dfcp.index.year == year
        cond2 = dfcp.index.month == month
        cond3 = dfcp.index.day == day
        dfcp1 = dfcp[cond1 & cond2 & cond3]
    elif (type(year)==int) & (type(month)==int):
        cond1 = dfcp.index.year == year
        cond2 = dfcp.index.month == month
        dfcp1 = dfcp[cond1 & cond2]
    elif type(year)==int:
        dfcp1 = dfcp[dfcp.index.year == year]
    else:
        dfcp1 = dfcp
    dfcp1.plot(kind = 'scatter', x='Opened_Int', y='Process_days', alpha = 0.2, c = 'm', figsize=(20,10))
    return


if __name__ == '__main__':
    file1 = '/Users/haowei/Documents/GN/Project/data_pool/Loan_data/LoanStats_2016Q1.csv'
    file2 = '/Users/haowei/Documents/GN/Project/data_pool/311/Case_Data_from_San_Francisco_311__SF311_.csv'
    df = read_csv_chunks_into_df(file2,10000, parse_date=False)
    explore_df(df)
    # get_unique(df)
    # get_unique(df)

    dt_list = ['Opened','Closed','Updated']
    dft = df.iloc[:10000,:]
    dft = to_datetime(dft, dt_list)
    explore_list = ['Status','Status Notes', 'Responsible Agency', 'Category', \
                 'Request Type', 'Request Details', 'Address', 'Supervisor District', \
                 'Neighborhood', 'Point', 'Source', 'Media URL' ]
    short_explore_list = ['Status', 'Responsible Agency', 'Category', 'Neighborhood', 'Source']
    get_value_counts(df, explore_list )

    dft1 = dft.copy()
    dft1['Process_time'] = dft1['Closed'] - dft1['Opened']
    dft1 = dft1[dft1['Process_time'].notnull()]
    dft1['Process_minutes'] = dft1['Process_time'].apply(days_to_minutes)
    dft1['Process_hours'] = dft1['Process_time'].apply(days_to_hours

    cate_val = get_sorted_category_value(dft1,'Category')
    req_type_val = get_sorted_category_value(dft1,'Request Type')

    dft_cat_dict = category_to_numer_dict(dft1, 'Category',cate_val)
    dft_req_type_dict = category_to_numer_dict(dft1, 'Request Type', req_type_val)

    dft_norm = dft1[dft1.Process_minutes<40000]
    dft_norm.Process_minutes.hist(bins=10)
    plt.show()
    dft_norm.Process_hours.hist()
    plt.show()

    dft_norm.plot(kind = 'scatter', x='Category', y='Process_hours', alpha = 0.4)
    dft_norm.plot(kind = 'scatter', x='Request Type', y='Process_hours', alpha = 0.4)
