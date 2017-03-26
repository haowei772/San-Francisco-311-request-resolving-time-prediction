import pandas as pd
import numpy as np
from collections import defaultdict
import matplotlib.pyplot as plt
import seaborn as sns

from pandas.tseries.holiday import USFederalHolidayCalendar as calendar
from datetime import date, datetime, time, timedelta
from scipy import stats
from DataCleaning import clean_data
import EDA

if __name__ == '__main__':
    # folder = '/Users/haowei/Documents/GN/Capstone/Capstone-project/data/'
    # filename = 'SF311.csv'
    # filepath = folder+filename
    # df = read_csv_chunks_into_df(filepath,10000, parse_date=False)
    # explore_df(df)
    # # get_unique(df)
    # # get_unique(df)
    #
    # dt_list = ['Opened','Closed','Updated']
    # dft = df.iloc[:10000,:]
    # dft = to_datetime(dft, dt_list)
    # explore_list = ['Status','Status Notes', 'Responsible Agency', 'Category', \
    #              'Request Type', 'Request Details', 'Address', 'Supervisor District', \
    #              'Neighborhood', 'Point', 'Source', 'Media URL' ]
    # short_explore_list = ['Status', 'Responsible Agency', 'Category', 'Neighborhood', 'Source']
    # get_value_counts(df, explore_list )
    #
    # dft1 = dft.copy()
    # dft1['Process_time'] = dft1['Closed'] - dft1['Opened']
    # dft1 = dft1[dft1['Process_time'].notnull()]
    # dft1['Process_minutes'] = dft1['Process_time'].apply(days_to_minutes)
    # dft1['Process_hours'] = dft1['Process_time'].apply(days_to_hours)
    #
    # cate_val = get_sorted_category_value(dft1,'Category')
    # req_type_val = get_sorted_category_value(dft1,'Request Type')
    #
    # dft_cat_dict = category_to_numer_dict(dft1, 'Category',cate_val)
    # dft_req_type_dict = category_to_numer_dict(dft1, 'Request Type', req_type_val)
    #
    # dft_norm = dft1[dft1.Process_minutes<40000]
    # dft_norm.Process_minutes.hist(bins=10)
    # plt.show()
    # dft_norm.Process_hours.hist()
    # plt.show()
    #
    # dft_norm.plot(kind = 'scatter', x='Category', y='Process_hours', alpha = 0.4)
    # dft_norm.plot(kind = 'scatter', x='Request Type', y='Process_hours', alpha = 0.4)
    # print 'Done'
    '''
    *****************************************************************
    From here: can be skipped because the valid cases have been stored in csv file
    *****************************************************************
    '''
    folder = '/Users/haowei/Documents/GN/Capstone/Capstone-project/data/'
    filename_original = 'SF311.csv'
    dft = import_data(folder, filename_original)
    dft_valid_reduced = clean_data(dft, folder)

    ''' verify the new csv files'''
    filename_open = 'SF311_still_open_raw.csv'
    filename_wrong_dates = 'SF311_wrong_dates_raw.csv'
    filename_duplicates = 'SF311_duplicates_raw.csv'
    filename_valid = 'SF311_valid_raw.csv'
    filename_reduced = 'SF311_valid_reduced.csv'
    ndf = pd.read_csv(folder+filename_open)
    print ndf.shape
    wdf = pd.read_csv(folder+filename_wrong_dates)
    print wdf.shape
    ddf = pd.read_csv(folder+filename_duplicates)
    print ddf.shape
    vdf = pd.read_csv(folder+filename_valid)
    print vdf.shape
    rdf = pd.read_csv(folder+filename_reduced)
    print rdf.shape

    '''Read data from new cleaned and reduced csv file'''
    folder = '/Users/haowei/Documents/GN/Capstone/Capstone-project/data/'
    filename_reduced = 'SF311_valid_reduced.csv'

    cfdf = get_prep_data(folder+filename_reduced)
    cfdf_cp = cfdf.copy()
    print 'reduced dataframe shape: ', cfdf.shape

    cfdf = add_features(cfdf)

    '''write the cases with engineered features to csv named SF311_engineered.csv'''
    filename_engineered = 'SF311_engineered.csv'
    cfdf.to_csv(folder+filename_engineered)
    '''
    *****************************************************************
    To here: can be skipped because the valid engineered cases have been stored in csv file
    *****************************************************************
    '''
    print 'Done'
