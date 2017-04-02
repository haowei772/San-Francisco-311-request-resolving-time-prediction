import pandas as pd
import numpy as np
from collections import defaultdict
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
from pandas.tseries.holiday import USFederalHolidayCalendar as calendar
from datetime import date, datetime, time, timedelta
from scipy import stats
from EDA import batch_process_categories, get_prep_data
from PremodelingProcess import train_vali_split, get_df_for_modeling, dump_object_to_pickle, add_dummy
import EDA
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

# def get_coordinates(df, coordinate_col):




'''test the KNN accuracy'''
def test_KNN(df, target_col, predictor_cols, test_size = 0.2, neighbors=3, random = 111):
    '''test KNN on the dataset with both target_col and predictor_col not missing'''
    '''df should have no missing values in both target_col and predictor_col'''
    d_train, d_test = train_test_df_split(df, test_size = test_size, random_seed = random)

    X_train = d_train[predictor_cols].values
    y_train = d_train[target_col].values.astype(int)
    X_test = d_test[predictor_cols].values
    y_test = d_test[target_col].values.astype(int)

    '''fit model'''
    neighbor = KNN_modle(X_train, y_train, neighbors=neighbors )

    '''predict '''
    yhat = neighbor.predict(X_test)
    # print y_test[:20]
    # print '*****'
    # print yhat[:20]
    acc = accuracy_score(y_test, yhat)
    print 'accuracy_score: ', acc
    return acc

def KNN_modle(X, y, neighbors=3 ):
    neighbor = KNeighborsClassifier(n_neighbors=neighbors)
    neighbor.fit(X, y)
    return neighbor

def get_component(components, strip = '()', sep = ','):
    '''
    returns a list of floats from a string
    string (1,2,3) will return int (1.0, 2.0, 3.0)
    strip means the string wanted to be removed, e.g., can be '()'
    '''
    if strip:
        components = str(components).translate(None,strip).split(sep)
    else:
        components = str(components).split(sep)
    results = []
    for component in components:
        results.append(float(component))
    return results

def prepare_df(df, target_col):
    '''fill missing value by simple way'''
    df = simple_fill_missing(df, [target_col])
    '''change target column to numeric values'''
    dict_target = batch_process_categories(df, [target_col])
    print dict_target.keys()
    '''get the key for target in the target value dictionary'''
    key_miss = [key for key in dict_target[target_col] if dict_target[target_col][key] == 'Missing'+target_col][0]
    return df, key_miss

'''add x and y to df with point'''
def add_predictors_columns(df, predictor_col):
    '''
    return tuple of 1. df with no missing predictor and the values of predictor have been moved to the seperated collumns, and 2. list of column names that are newly added
    '''
    dfcp = df.copy()
    print dfcp.head(2)
    df_predict = dfcp[dfcp[predictor_col].notnull()]
    print df_predict.iloc[0][predictor_col] # can not use ix because index is already integer
    numbers = get_component(df_predict.iloc[0][predictor_col], strip = '()', sep = ',')
    predictors_col_names = []
    for i in range(len(numbers)):
        df_predict[str(i)] = df_predict[predictor_col].apply(lambda x: get_component(x)[i])
        predictors_col_names.append(str(i))
    return df_predict, predictors_col_names

def get_knn_labels(df, target_col, predictor_cols, key_miss, neighbors=3 ):
    '''get the predicted labels of target with missing values'''
    '''df should have no missing predictors'''
    df_not_miss = df[df[target_col] != key_miss]
    df_miss = df[df[target_col] == key_miss]
    X_train = df_not_miss[predictor_cols].values
    y_train = df_not_miss[target_col].values.astype(int)
    X_test = df_miss[predictor_cols].values

    neighbor = KNeighborsClassifier(n_neighbors=neighbors)
    neighbor.fit(X_train, y_train)
    yhat = neighbor.predict(X_test)
    return yhat

def integration(df, target_col, predictor_col, key_miss, labels):
    '''integration of labels to the original df with missing valued filled and changed to numeric values'''
    df1 = df.copy()
    condition1 = df1[target_col] == key_miss
    condition2 = df1[predictor_col].notnull()
    df1.ix[condition1 & condition2, target_col] = labels
    return df1

'''impute target y based on predictors X'''
def impute_missing_knn(df, target_col, predictor_col, neighbors =3):
    '''fill missing value by simple way'''
    '''change target column to numeric values'''
    '''get the key for target in the target value dictionary'''
    df, key_miss = prepare_df(df, target_col)
    '''get the df_predict which has no predictor missing, and change predictor to columns of predictors'''
    df_predict, predictors_col_names = add_predictors_columns(df, predictor_col)
    '''get the predicted labels of target with missing values'''
    labels = get_knn_labels(df_predict, target_col, predictors_col_names, key_miss, neighbors=3)
    '''integration of labels to the original df with missing valued filled and changed to numeric values'''
    df  = integration(df, target_col, predictor_col, key_miss, labels)
    return df

folder = '/Users/haowei/Documents/GN/Capstone/Capstone-project/data/'
filename_engineered = 'SF311_engineered.csv'
target_col = 'Neighborhood'
predictor_col = 'Point'
df = get_prep_data(folder+filename_engineered)
EDA.get_missing(df)
df1 = impute_missing_knn(df, target_col, predictor_col, neighbors =3)
'''$$$$$$$$$$$$$$$$$$$$ End Missing Value Handling $$$$$$$$$$$$$$$$$$$$'''
