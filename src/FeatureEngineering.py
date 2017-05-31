import pandas as pd
import numpy as np

from collections import defaultdict
from pandas.tseries.holiday import USFederalHolidayCalendar as calendar
from datetime import date, datetime, time, timedelta
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
from PremodelingProcess import train_vali_split, get_df_for_modeling, dump_object_to_pickle, add_dummy
from DataCleaning import import_data

def add_features(df):
    '''
    Add new features to the dataframe, including Day of week, Month, Year, Weekend, Holiday
    INPUT: df - a dataframe
    OUTPUT: a dataframe with added columns
    '''
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

    df1['Open_Time'] = df1['Opened'].astype(int).astype(float)/(10**16)
    df1['Request Topic'] = df1['Request Type']
    return df1

def simple_fill_missing(df, columns):
    '''
    Simple way to fill the missing values: add a new 'Missing category for categorical feature
    and add -1 for numerical feature, e.g., the dicstrict number.
    INPUT: df - a dataframe, columns - list of column names
    OUTPUT: a dataframe
    '''
    df1 = df.copy()
    for column in columns:
        if df1[column].dtype == float:
            df1[column].fillna(-1.0, inplace = True)
        else:
             df1[column].fillna('Missing '+column, inplace=True)
    return df1

def test_KNN(df, target_col, predictor_cols, test_size = 0.2, neighbors=3, random = 111):
    '''
    Test the KNN algorithm for filling missing values using the test dataset
    (target_col and predictor_col not missing)
    INPUT: df - a dataframe, target_col - name of column with missing value to be filled in string,
    test_size - percentage of the dataset used for testing in float, neighbors - number of neighbors used in KNN,
    random - number to set the random state for dataset spliting
    OUTPUT: accuracy score in float
    '''
    d_train, d_test = train_test_df_split(df, test_size = test_size, random_seed = random)

    X_train = d_train[predictor_cols].values
    y_train = d_train[target_col].values.astype(int)
    X_test = d_test[predictor_cols].values
    y_test = d_test[target_col].values.astype(int)

    '''fit model'''
    neighbor = KNN_modle(X_train, y_train, neighbors=neighbors )

    '''make prediction '''
    yhat = neighbor.predict(X_test)
    acc = accuracy_score(y_test, yhat)
    return acc

def KNN_modle(X, y, neighbors=3 ):
    '''
    Build a KNN classification model
    INPUT: X and y - dataframe and series of predictors and label, neighbors - number of neighbors
    OUTPUT: fitted model object
    '''
    neighbor = KNeighborsClassifier(n_neighbors=neighbors)
    neighbor.fit(X, y)
    return neighbor

def get_component(components, strip = '()', sep = ','):
    '''
    Returns a list of floats from a string, e.g., string (1,2,3) will return int (1.0, 2.0, 3.0)
    INPUT: components - a string containing numbers to be processed,
    strip - the string need to be removed, e.g., '()', sep - the string as the separator
    OUTPUT: list of floats
    '''
    if strip:
        components = str(components).translate(None,strip).split(sep)
    else:
        components = str(components).split(sep)
    results = []
    for component in components:
        results.append(float(component))
    return results

# def prepare_df(df, target_col):
#
#     '''fill missing value by simple way'''
#     df = simple_fill_missing(df, [target_col])
#     '''change target column to numeric values'''
#     dict_target = batch_process_categories(df, [target_col])
#     print dict_target.keys()
#     '''get the key for target in the target value dictionary'''
#     key_miss = [key for key in dict_target[target_col] if dict_target[target_col][key] == 'Missing'+target_col][0]
#     return df, key_miss

# '''add x and y to df with point'''
# def add_predictors_columns(df, predictor_col):
#     '''
#     return tuple of 1. df with no missing predictor and the values of predictor have been moved to the seperated collumns, and 2. list of column names that are newly added
#     '''
#     dfcp = df.copy()
#     print dfcp.head(2)
#     df_predict = dfcp[dfcp[predictor_col].notnull()]
#     print df_predict.iloc[0][predictor_col] # can not use ix because index is already integer
#     numbers = get_component(df_predict.iloc[0][predictor_col], strip = '()', sep = ',')
#     predictors_col_names = []
#     for i in range(len(numbers)):
#         df_predict[str(i)] = df_predict[predictor_col].apply(lambda x: get_component(x)[i])
#         predictors_col_names.append(str(i))
#     return df_predict, predictors_col_names

def get_knn_labels(df, target_col, predictor_col, key_miss, neighbors=3 ):
    '''
    Returns a series of predicted labels based on KNN algorithm (df should have no missing predictors).
    INPUT: df - a dataframe, target_col - name of column with missing value to be filled in string,
    predictor_cols - name of columns used as predictors, key_miss - a string indicator of missing value,
    neighbors - number of neighbors used in KNN
    OUTPUT: a series of predicted labels
    '''
    df_not_miss = df[df[target_col] != key_miss]
    df_miss = df[df[target_col] == key_miss]
    X_train = df_not_miss[predictor_col].values
    y_train = df_not_miss[target_col].values.astype(int)
    X_test = df_miss[predictor_col].values

    neighbor = KNeighborsClassifier(n_neighbors=neighbors)
    neighbor.fit(X_train, y_train)
    yhat = neighbor.predict(X_test)
    return yhat

def integration(df, target_col, predictor_col, key_miss, labels):
    '''
    Integration of labels to the original df with missing values
    INPUT: df - a dataframe, target_col - name of column with missing value to be filled in string,
    predictor_col - name of column used as predictor, key_miss - a string indicator of missing value,
    labels - a series of predicted labels
    OUTPUT: dataframe with missing values filled using KNN
    '''
    df1 = df.copy()
    condition1 = df1[target_col] == key_miss
    condition2 = df1[predictor_col].notnull()
    df1.ix[condition1 & condition2, target_col] = labels
    return df1


def impute_missing_knn(df, target_col, predictor_col, neighbors =3):
    '''
    Impute missing values in target column based on predictor column using KNN
    INPUT: df - a dataframe, target_col - name of column with missing value to be filled in string,
    predictor_col - name of column used as predictor, neighbors - number of neighbors
    OUTPUT: dataframe with missing values filled using KNN
    '''
    '''1. Fill missing value by simple way, change target column to numeric values
    and get the key for target in the target value dictionary'''
    df, key_miss = prepare_df(df, target_col)

    '''2. Get the df_predict which has no predictor missing, and change
    predictor to columns of predictors'''
    df_predict, predictors_col_names = add_predictors_columns(df, predictor_col)

    '''3. Get the predicted labels of target with missing values'''
    labels = get_knn_labels(df_predict, target_col, predictors_col_names, key_miss, neighbors=3)

    '''4. Integration of labels to the original df with missing valued filled and changed to numeric values'''
    df  = integration(df, target_col, predictor_col, key_miss, labels)
    return df

#
# filepath = '../data/SF311.csv'
# df = import_data(filepath)
# target_col = 'Neighborhood'
# predictor_col = 'Point'
# #df = get_prep_data(folder+filename_engineered)
# #EDA.get_missing(df)
# df1 = impute_missing_knn(df, target_col, predictor_col, neighbors =3)
