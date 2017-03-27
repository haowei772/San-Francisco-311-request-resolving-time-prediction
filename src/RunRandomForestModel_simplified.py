from MachineLearningModel import RandomForestRegressor_model, GradientBoostingRegressor_model #, plot_importance
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
from PremodelingProcess import train_vali_split, get_df_for_modeling, dump_object_to_pickle
import EDA
import os
from sklearn.model_selection import cross_val_score


if __name__ == '__main__':
    '''Check if there is pickle files of dataframe and category dictionaries ready for load'''
    df_pickle_filename = '../data/df_tr.pickle'
    dict_pickle_filename = '../data/category_dict.pickle'
    rfr_model_simplified_pickle_filename = '../results/rfr_model_simplified.pickle'
    filename_train = '../data/SF311_train.csv'

    df_tr, category_dictionaries = get_df_for_modeling(df_pickle_filename, dict_pickle_filename, filename_train)

    '''simplify the the model'''
    print 'simplified model'
    kept_list = ['Responsible Agency', 'Supervisor District', 'Category','Request Type', 'Neighborhood', 'Process_days',  'Opened_Int']
    df_tr = df_tr[kept_list]
    # limit = int(0.2*len(df_tr))
    # df_tr = df_tr[limit:]
    print df_tr.shape
    print 'start training ...'
    X_train, X_test, y_train, y_test = train_vali_split(df_tr, 'Process_days', test_size = 0.2, random_seed = 122)
    print 'X_train: ', len(X_train)
    print 'X_test: ', len(X_test)
    rfr_model, yhat_randomF, randomF_rscore, oob_score = RandomForestRegressor_model(X_train, X_test, y_train, y_test, 100)
    print 'Done with training.'
    # '''save the model to a pickle file'''
    # dump_object_to_pickle(rfr_model, rfr_model_simplified_pickle_filename)
    mse_randomF = mean_squared_error(y_test, yhat_randomF)

    print 'randomF_rscore: ',randomF_rscore
    print 'oob_score: ',oob_score
    print 'mse_randomF: ', mse_randomF
    '''get training score'''
    yhat_train = rfr_model.predict(X_train)
    print 'training r2_score: ',r2_score(y_train, yhat_train)

    '''get k-fold cross validation scores'''
    print 'Start k-fold cross validation'
    cross_val_scores = cross_val_score(rfr_model, X_train, y_train, cv=3)
    print 'cross_val_scores: ', cross_val_scores
