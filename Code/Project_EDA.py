import pandas as pd
import numpy as np
from collections import defaultdict
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()

def explore(file):
    def explore_file(file):
    df = pd.read_csv(file)
    #df = pd.read_csv(file, parse_dates= ['Opened','Closed','Updated'], infer_datetime_format=True)
    #df = pd.read_csv(file, skiprows=1,sep = ' ', error_bad_lines=False,skiprows=1, parse_dates= ['issue_d','last_pymnt_d', 'last_credit_pull_d'], infer_datetime_format=True)
    explore_df(df)
    return df

def read_csv_chunks_into_df(file_path, chunk_size, parse_date=False, date_col =None):
    if parse_date:
        chunks = pd.read_csv(file_path, parse_dates= date_col, infer_datetime_format=True, chunksize = chunk_size )
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
    print 'Total missing data ', df2.isnull().sum().sum()

def drop_na_row(df,feature):
    df = df.ix[df[feature].notnull(), :]
    return df

def get_value_counts(df, feature_list):
    for feature in feature_list:
        print '************ '+feature+' value counts ***********'
        print df[feature].value_counts(dropna = False)
    return

def parsedate(df, columns, time_format):
    '''parse list of coloumns to pd.datetime object'''
    for column in columns:
        df[column] = pd.to_datetime(df[column], format = time_format)
    return df

def days_to_minutes(td):
    return  td.total_seconds()//60#(td.seconds//60)%60

def days_to_hours(td):
    hours = td.total_seconds()/3600#(td.seconds//60)%60
    return np.round(hours,1)

def get_sorted_category_value(df, category):
    ''' returns sorted categorical values based on the mean process_hours '''
    dfm = df.groupby(category).mean()
    dfm = dfm.sort_values('Process_hours')
    return dfm.index

def category_to_numer_dict(df, category, values):
    '''Change a categorical column to numeric and save the categorical values in a dictionary for later reference'''
    dict = defaultdict(str)
    for i,value in enumerate(values):
        dict[i] = value # store the categorical values in a dictionary for later reference
        df.ix[df[category]==value, category] = i
    return dict

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
