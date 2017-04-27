from MachineLearningModel import RandomForestRegressor_model, GradientBoostingRegressor_model #, plot_importance
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
from PremodelingProcess import train_vali_split, get_df_for_modeling, dump_object_to_pickle, get_X_y
import numpy as np
import EDA
import os
from sklearn.model_selection import cross_val_score


if __name__ == '__main__':
    '''Check if there is pickle files of dataframe and category dictionaries ready for load'''
    df_train_filename = '../data/SF311_df_train_kmeans.csv'
    df_test_filename = '../data/SF311_df_test_kmeans.csv'


    # filename_train = '../data/SF311_train_KNN.csv'
    #rfr_model_pickle_filename = '../data/rfr_model_KNN.pickle'
    #rfr_model_pickle_filename = '../data/rfr_model_ln.pickle'

    # df_tr, category_dictionaries = get_df_for_modeling(df_pickle_filename, dict_pickle_filename, filename_train)

    '''use log transformation to normalize the dependent variable Process_days'''
    # df_tr['Process_days'] = np.log(df_tr['Process_days'])
    # # print df_tr['Process_days'][:10]

    df_train  = EDA.get_prep_data(df_train_filename)
    df_test  = EDA.get_prep_data(df_test_filename)

    use_features = ['Responsible Agency', 'Category',\
            'Supervisor District', 'Neighborhood', 'Source', 'Process_days', \
            'Day_Of_Week', 'Month', 'Year', 'Weekend', 'Holiday', 'Before_Holiday', 'Open Time' , 'kmeans']
    # use_features = ['Responsible Agency', 'Category','Request Topic'\
    #             'Supervisor District', 'Neighborhood', 'Source', 'Process_days', \
    #             'Day_Of_Week', 'Month', 'Year', 'Weekend', 'Holiday', 'Before_Holiday', 'Open Time' , 'kmeans']
    # X_train, X_test, y_train, y_test = train_vali_split(df_tr, 'Process_days', test_size = 0.15, random_seed = 100)
    df_train = df_train[use_features]
    df_test = df_test[use_features]

    # cate_list = ['Category','Responsible Agency','Request Topic','Neighborhood','Source']
    cate_list = ['Category','Responsible Agency','Neighborhood','Source']
    cate_dict_train = EDA.batch_process_categories(df_train, cate_list)
    cate_dict_test = EDA.batch_process_categories(df_test, cate_list)

    X_train, y_train = get_X_y(df_train, 'Process_days')
    X_test, y_test = get_X_y(df_test, 'Process_days')
    print 'X_train: ', len(X_train)
    print 'X_test: ', len(X_test)
    rfr_model, yhat_randomF, randomF_rscore, oob_score = RandomForestRegressor_model(X_train, X_test, y_train, y_test, 100)

    mse_randomF = mean_squared_error(y_test, yhat_randomF)

    print 'randomF_rscore: ',randomF_rscore
    print 'oob_score: ',oob_score
    print 'mse_randomF: ', mse_randomF
    '''get training score'''
    yhat_train = rfr_model.predict(X_train)
    print 'training r2_score: ',r2_score(y_train, yhat_train)

    # '''get k-fold cross validation scores'''
    # print 'Start k-fold cross validation'
    # cross_val_scores = cross_val_score(rfr_model, X_train, y_train, cv=3)
    # print 'cross_val_scores: ', cross_val_scores
    # '''save the model to a pickle file'''
    # dump_object_to_pickle(rfr_model, rfr_model_pickle_filename)
