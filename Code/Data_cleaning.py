import pandas as pd
import numpy as np
from collections import defaultdict

'''$$$$$$$$$$$$$$$$$$$$ Start Cleaning Data $$$$$$$$$$$$$$$$$$$$'''
def clean_data(dft):
    '''remove and save the cases that are not closed'''
    dft_still_open = dft[dft['Closed'].isnull()] # cases that not closed
    filename_open = 'SF311_still_open_raw.csv'
    dft_still_open_csv_path = folder + filename_open
    dft_still_open.to_csv(dft_still_open_csv_path) # dft_still_open.csv contains cases that not closed

    '''calculate the process time '''
    condition = dft['Closed'].notnull()
    dft_closed = dft[condition] # cases that are closed
    dft_closed['Process_days'] = dft_closed['Closed'] - dft_closed['Opened']
    dft_closed['Process_hours'] = dft_closed['Process_days'].apply(days_to_hours)

    ''' remove cases with process time <= 0 hours and save theses cases '''
    dft_wrong_dates = dft_closed[dft_closed['Process_hours'] <= 0]
    filename_wrong_dates = 'SF311_wrong_dates_raw.csv'
    dft_wrong_dates_csv_path = folder + filename_wrong_dates
    dft_wrong_dates.to_csv(dft_wrong_dates_csv_path)
    # dft_wrong_dates_raw.csv contains cases that have wrong dates: closed before opened'''re
    dft_right_dates = dft_closed[dft_closed['Process_hours'] > 0]

    ''' remove duplicated cases and save theses cases '''
    dft_duplicates, dft_valid = check_word_in_col(dft_right_dates, 'Status Notes', 'Duplicate')
    filename_duplicates = 'SF311_duplicates_raw.csv'
    dft_duplicates_csv_path = folder + filename_duplicates
    dft_duplicates.to_csv(dft_duplicates_csv_path) # dft_duplicates_raw.csv contains cases that are duplicated

    '''convert Process_days to float'''
    dft_valid['Process_days'] = dft_valid['Process_hours']/24.0

    '''save raw valid cases'''
    filename_valid = 'SF311_valid_raw.csv'
    dft_valid_csv_path = folder + filename_valid
    dft_valid.to_csv(dft_valid_csv_path)

    '''remove unnecessary columns and save the cases to csv file'''
    drop_col = ['Updated','Status', 'Media URL']
    dft_valid_reduced = dft_valid.drop(drop_col, axis =1)
    filename_reduced = 'SF311_valid_reduced.csv'
    dft_valid_reduced_csv_path = folder + filename_reduced
    dft_valid_reduced.to_csv(dft_valid_reduced_csv_path)

    print 'Number of original cases: ', len(dft)
    print 'Cases that are not closed: ', len(dft_still_open)
    print 'Cases with process time <= 0: ', len(dft_wrong_dates)
    print 'Cases with process time > 0: ', len(dft_right_dates)
    print 'Duplicated cases: ', len(dft_duplicates)
    print 'Valid cases: ', len(dft_valid)
    return dft_valid_reduced

'''######## this can be a short lambda expression########'''
def get_str_list(string):
    '''convert to a list of string'''
    return str(string).split()

'''######## this can be a short lambda expression########'''
def check_dup(str_list):
    '''check if word 'Duplicate' is in the string list'''
    return 'Duplicate' in str_list

def check_word_in_col(df, column, word):
    '''check if a word in the column, returns a tuple of dataframes,
    the first one contains the word and second one does not'''
    df1 = df.copy()
    get_str_list = lambda x: str(x).split()
    check_dup = lambda x: word in x

    df1[column+'1'] = df1[column].apply(get_str_list) # turn df1[column] into a list of strings
    cond = df1[column+'1'].apply(check_dup) # check if df1[column+'1'] contains the word
    df_found = df[cond]
    df_not_found = df[~cond]
    return df_found, df_not_found
'''$$$$$$$$$$$$$$$$$$$$ End Cleaning Data $$$$$$$$$$$$$$$$$$$$'''
