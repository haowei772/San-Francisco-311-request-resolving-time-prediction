from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.grid_search import GridSearchCV
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import linear_model
from sklearn.metrics import mean_squared_error
import pandas as pd
import numpy as np
from collections import defaultdict
# import matplotlib.pyplot as plt
# import seaborn as sns

from pandas.tseries.holiday import USFederalHolidayCalendar as calendar
from datetime import date, datetime, time, timedelta
from scipy import stats
import EDA
import pickle
import os

'''$$$$$$$$$$$$$$$$$$$$ Start Pre-modeling Process $$$$$$$$$$$$$$$$$$$$'''
def add_dummy(df, target_col):
    d = pd.get_dummies(df[target_col])
    d = d.drop(d.columns[-1], axis = 1)
    df_list = [df,d]
    df = pd.concat(df_list,axis =1)
    df = df.drop(target_col, axis =1)
    return df


def train_test_df_split(df, test_size = 0.2, random_seed = 111):
    np.random.seed(seed = random_seed)
    df['Flag'] = np.random.random(size = len(df)) <= test_size
    df_train = df[~df['Flag']]
    df_test = df[df['Flag']]
    df_train.drop('Flag', axis=1, inplace = True)
    df_test.drop('Flag', axis=1, inplace = True)
    return df_train, df_test

'''use the training dataset and do another training validation split'''

'''Setup data with simple train/test split'''
def train_vali_split(df, target_col, test_size = 0.2, random_seed = 100):
    v_features = df.columns.tolist()
    v_features = v_features[:]
    del v_features[v_features.index(target_col)]

    X = df.ix[:, v_features]
    y = df[target_col].astype('float')

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_seed)
    return X_train, X_test, y_train, y_test

def get_X_y(df, target_col):
    v_features = df.columns.tolist()
    v_features = v_features[:]
    del v_features[v_features.index(target_col)]

    X = df.ix[:, v_features]
    y = df[target_col].astype('float')
    return X, y

def preprocess_data(df):

    '''Select features'''
    # print df.columns.values
    use_features = ['Responsible Agency', 'Category','Request Topic',\
                'Supervisor District', 'Neighborhood', 'Source', 'Process_days', \
                'Day_Of_Week', 'Month', 'Year', 'Weekend', 'Holiday', 'Before_Holiday', 'Open Time' ]
    # '''temporay use'''
    # use_features = ['Responsible Agency', 'Category','Request Topic',\
    #             'Supervisor District', 'Neighborhood', 'Source', 'Process_days', \
    #             'Day_Of_Week', 'Month', 'Year', 'Weekend', 'Holiday', 'Before_Holiday', 'Opened_Int' ]
    # # '''test the  features '''
    # # use_features = ['Responsible Agency', 'Category','Request Topic',\
    #             'Supervisor District', 'Neighborhood', 'Source', 'Process_days', \
    #             'Day_Of_Week', 'Month', 'Year', 'Weekend', 'Holiday' ]

    df = df[use_features]
    '''scale feature Opened_Int, will not need this line after correct the early point'''
    # df['Opened_Int'] = df['Opened_Int']*1./10**16
    #print df['Open_Time'].dtype
    '''convert categorical features to numerical'''
    cate_list = ['Category','Responsible Agency','Request Topic','Neighborhood','Supervisor District','Source']
    # cate_list = ['Category','Responsible Agency','Neighborhood','Source'] #  for NLP

    #print 'no open-time and topic'
    cate_dict = EDA.batch_process_categories(df, cate_list)
    return df, cate_dict

def load_object_from_pickle(filename):
    '''Load the pickled dataframe'''
    file1 = open(filename, 'rb')
    obj = pickle.load(file1)
    file1.close()
    '''
    # shorter working version
    with open('filename', 'rb') as file1:
    obj = pickle.load(file1)
    '''
    return obj

def dump_object_to_pickle(obj,filename):
    #Pickle the dataframe.
    f = open(filename, 'wb')
    pickle.dump(obj, f, protocol=pickle.HIGHEST_PROTOCOL)
    f.close()

    '''
    # shorter working version
    with open('filename', 'wb') as f:
    pickle.dump(obj, file1, protocol=pickle.HIGHEST_PROTOCOL)

    pickle a dictionary can be problematic, can use dill to dump instead. The signature is the same:
    import dill
    with open('filename', 'w) as f:
       dill.dump(obj, f)
    '''
    return

def get_df_for_modeling(df_pickle_filename, dict_pickle_filename, filename_train):
    if os.path.exists(df_pickle_filename) and os.path.exists(dict_pickle_filename):
        df = load_object_from_pickle(df_pickle_filename)
        print 'get df from pickle'
        category_dictionaries = load_object_from_pickle(dict_pickle_filename)
    else:
        '''Read data from train csv file'''
        print 'get data from csv file'
        df = EDA.get_prep_data(filename_train)
        df, category_dictionaries = preprocess_data(df)
        # '''EBS out of space'''
        '''save df and category_dictionaries to pickle files'''
        dump_object_to_pickle(df,df_pickle_filename)
        dump_object_to_pickle(category_dictionaries, dict_pickle_filename)
    return df,category_dictionaries

def get_df_for_engineer(filename_pickle, filename_train):
    if os.path.exists(filename_pickle):
        print 'get df from pickle'
        df = load_object_from_pickle(filename_pickle)
    else:
        '''Read data from train csv file'''
        print 'get data from csv file'
        df = EDA.get_prep_data(filename_train)
        '''save df to pickle files'''
        dump_object_to_pickle(df,filename_pickle)
    return df

def process_data_for_survival_model(df, test_size = 0.2, random_state = 222):
    df['Event'] = 1
    df = df.astype(float)
    df_train, df_test = train_test_df_split(df, test_size = test_size, random_seed = random_state)
    return df_train, df_test
'''$$$$$$$$$$$$$$$$$$$$ End Pre-modeling Process $$$$$$$$$$$$$$$$$$$$'''
