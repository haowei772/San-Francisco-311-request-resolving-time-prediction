import pandas as pd
import numpy as np
from collections import defaultdict

from pandas.tseries.holiday import USFederalHolidayCalendar as calendar
from datetime import date, datetime, time, timedelta

'''$$$$$$$$$$$$$$$$$$$$ Start Feature Engineering $$$$$$$$$$$$$$$$$$$$'''
def add_features(df):
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
    return df1

def get_oneway_anova(df, target_col, group_col, group_list=False):
    if group_list:
        groups = group_list
    else:
        groups = list(df[group_col].unique())
    datasets =[]
    for component in groups:
        df_temp = df[df[group_col] == component]
        datasets.append(np.array(df_temp[target_col]))
    f_val, p_val = stats.f_oneway(*datasets)
    print "One-way ANOVA P =", p_val
    return p_val

def add_current_open(df):
    '''add column Current_Open which has the number of current open cases'''
    def get_open_cases(opt):
        condition1 = df['Opened'] < opt
        condition2 = df['Closed'] > opt
        open_cases = df[condition1 & condition2]
        return len(open_cases)
    df['Current_Open'] = df['Opened'].apply(get_open_cases)
    return df

def create_pilot(df, folder, filename):
    '''Create a pilot dataset of most recent 100000 cases for preliminary
    modeling and feature engineering, save as SF311_pilot.csv '''
    pilot = df.iloc[:100000,:]
    pilot.to_csv(folder+filename_pilot)
    return
'''$$$$$$$$$$$$$$$$$$$$ End Feature Engineering $$$$$$$$$$$$$$$$$$$$'''
