import pandas as pd
import numpy as np
from collections import defaultdict

from pandas.tseries.holiday import USFederalHolidayCalendar as calendar
from datetime import date, datetime, time, timedelta
from scipy import stats

'''$$$$$$$$$$$$$$$$$$$$ Start Missing Value Handling $$$$$$$$$$$$$$$$$$$$'''
def two_category_missing_info(df, category1, category2):
    condition1 = df[category1].isnull()
    condition2 = df[category2].isnull()
    both = len(df[condition1 & condition2])
    c1_only = len(df[condition1 & (~condition2)])
    c2_only = len(df[(~condition1) & (condition2)])
    neither = len(df[(~condition1) & (~condition2)])
    print "There are {0} cases missing both {1} and {2}.".format(both, category1, category2)
    print "There are {0} cases only missing {1} but not {2}.".format(c1_only, category1, category2)
    print "There are {0} cases only missing {2} but not {1}.".format(c2_only, category1, category2)
    print "There are {0} cases missing neither {1} nor {2}.".format(neither, category1, category2)
    print '***********'
    print df[condition1 & condition2].head(2)
    print '***********'
    print df[condition1 & (~condition2)].head(2)
    print '***********'
    print df[(~condition1) & (condition2)].head(2)
    return

def fill_missing_by_copy(df,category1, category2 ):
    '''1. copy category2 to missing values of category1'''
    df[category1].fillna(df[category2], inplace = True)

    '''2. fill the rest missing category1 values with 'Missing'''
    df[category1].fillna('Missing', inplace = True)
    '''both request type and details are missing, should be filled with Missing'''

    '''3. copy category1 to missing values of category2'''
    df[category2].fillna(df[category1], inplace = True)
    return df

def simple_fill_missing(df, columns):
    for column in columns:
        if df[column].dtype == float:
            df[column].fillna(-1.0, inplace = True)
        else:
             df[column].fillna('Missing'+column, inplace=True)
    return df

def impute_neighbor_knn():
    pass


'''$$$$$$$$$$$$$$$$$$$$ End Missing Value Handling $$$$$$$$$$$$$$$$$$$$'''
