import pandas as pd
import numpy as np
from collections import defaultdict

def clean_data(dft, folder):
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
