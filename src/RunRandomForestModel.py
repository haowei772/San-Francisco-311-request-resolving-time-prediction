from MachineLearningModel import RandomForestRegressor_model, GradientBoostingRegressor_model #, plot_importance
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
from PremodelingProcess import train_vali_split, get_df_for_modeling, dump_object_to_pickle
import numpy as np
import EDA
import os
from sklearn.model_selection import cross_val_score


if __name__ == '__main__':
    '''Check if there is pickle files of dataframe and category dictionaries ready for load'''
    df_pickle_filename = '../data/df_tr.pickle'
    dict_pickle_filename = '../data/category_dict.pickle'

    rfr_model_pickle_filename = '../data/rfr_model.pickle'
    filename_train = '../data/SF311_train.csv'

    # filename_train = '../data/SF311_train_KNN.csv'
    #rfr_model_pickle_filename = '../data/rfr_model_KNN.pickle'
    #rfr_model_pickle_filename = '../data/rfr_model_ln.pickle'

    df_tr, category_dictionaries = get_df_for_modeling(df_pickle_filename, dict_pickle_filename, filename_train)

    '''use log transformation to normalize the dependent variable Process_days'''
    # df_tr['Process_days'] = np.log(df_tr['Process_days'])
    # # print df_tr['Process_days'][:10]

    X_train, X_test, y_train, y_test = train_vali_split(df_tr, 'Process_days', test_size = 0.15, random_seed = 100)
    print 'X_train: ', len(X_train)
    print 'X_test: ', len(X_test)
    rfr_model, yhat_randomF, randomF_rscore, oob_score = RandomForestRegressor_model(X_train, X_test, y_train, y_test, 150)

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
