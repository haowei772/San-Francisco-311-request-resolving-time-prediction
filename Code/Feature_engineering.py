import pandas as pd
import numpy as np
from collections import defaultdict

from pandas.tseries.holiday import USFederalHolidayCalendar as calendar
from datetime import date, datetime, time, timedelta

def create_pilot(df, folder, filename):
     
    pilot = df.iloc[-100000:,:]
    pilot.to_csv(folder+filename_pilot)
    return

def add_features(df):
    df1 = df.copy()
    '''Add features: Day of week, Month, Weekend '''
    df1['Day_Of_Week'] = df1['Opened'].dt.dayofweek
    df1['Month'] = df1['Opened'].dt.month
    df1['Weekend'] = (df1['Day_Of_Week'].isin((5,6))).astype(int) # if the open day is at weekend

    '''Add feature Holiday and Before_Holiday'''
    cal = calendar()
    holidays = cal.holidays()
    # holidays = cal.holidays(start=cfdf['Opened'].min(), end=cfdf['Opened'].max())
    df1['Holiday'] = ((df1['Opened'].dt.date).astype('datetime64').isin(holidays)).astype(int)
    df1['Before_Holiday'] = (((df1['Opened'].dt.date).astype('datetime64')+timedelta(days = 1)).isin(holidays)).astype(int)
    num_of_holiday = len(df1[df1['Holiday'] == 1])
    num_of_before_holiday = len(df1[df1['Before_Holiday'] == 1])

    print 'Total bumber of cases on holiday: ', num_of_holiday
    print 'Total bumber of cases before holiday: ', num_of_before_holiday
    #cfdf['date2'] = (cfdf['Opened'].dt.date).astype('datetime64')+timedelta(days = 1)
    return df1

def add_current_open(df):
    '''add column Current_Open which has the number of current open cases'''
    def get_open_cases(opt):
        condition1 = df['Opened'] < opt
        condition2 = df['Closed'] > opt
        open_cases = df[condition1 & condition2]
        return len(open_cases)
    df['Current_Open'] = df['Opened'].apply(get_open_cases)
    return df
