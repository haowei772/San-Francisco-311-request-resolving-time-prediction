from MachineLearningModel import RandomForestRegressor_model, GradientBoostingRegressor_model #, plot_importance
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
from PremodelingProcess import train_vali_split, get_df_for_modeling, dump_object_to_pickle, train_test_df_split, get_df_for_modeling_topic
import EDA
import os
from sklearn.model_selection import cross_val_score
from NLPProcess import NLPProcessor
from FeatureEngineering import add_current_open

if __name__ == '__main__':


    # filename_engineer = '../data/SF311_engineered.csv'
    # filename_engineer_new = '../data/SF311_engineered_open_case.csv'
    # df_engi = EDA.get_prep_data(filename_engineer)
    # print 'add features ...'
    # df_engi = add_current_open(df_engi)
    # de_engi.to_csv()


    '''Check if there is pickle files of dataframe and category dictionaries ready for load'''
    df_pickle_filename = '../data/df_tr.pickle'
    dict_pickle_filename = '../data/category_dict.pickle'
    #rfr_model_pickle_filename = '../data/rfr_model.pickle'
    filename_train = '../data/SF311_train.csv'

    #df_tr, category_dictionaries = get_df_for_modeling_topic(filename_train)
    df_tr, category_dictionaries = get_df_for_modeling(df_pickle_filename, dict_pickle_filename,filename_train)

    df_train, df_test = train_test_df_split(df_tr, test_size = 0.2, random_seed = 111)
    print 'df_train: ', len(df_train), ' df_test: ', len(df_test)
    print df_train.head(1)

    #target_col = 'Request Topic'
    target_col = 'Request Topic'
    nlpp = NLPProcessor(100)
    print 'fitting kmeans...'
    nlpp.fit_transform(df_train, target_col)

    print 'predicting training labels...'
    kmeans_labels_train = nlpp.get_kmeans_train_labels()
    print 'predicting testing labels...'
    kmeans_labels_test = nlpp.transform(df_test, target_col)
    print df_train.head(10)
    print 'kmeans_labels_train: ', kmeans_labels_train[:10]
    print '***************************'
    print df_test.head(10)
    print 'kmeans_labels_test: ', kmeans_labels_test[:10]

    df_train['kmeans'] = kmeans_labels_train
    df_test['kmeans'] = kmeans_labels_test

    print 'df_train columns: ',df_train.columns.values
    print 'df_test columns: ',df_test.columns.values
    df_train_kmeans_filename = '../data/df_train_kmeans.csv'
    df_test_kmeans_filename = '../data/df_test_kmeans.csv'
    df_train.to_csv(df_train_kmeans_filename)
    df_test.to_csv(df_test_kmeans_filename)



    # X_train, y_train = get_X_y(df_train, 'Process_days')
    # X_test, y_test = get_X_y(df_test, 'Process_days')
    # print 'X_train: ', len(X_train)
    # print 'X_test: ', len(X_test)
    # rfr_model, yhat_randomF, randomF_rscore, oob_score = RandomForestRegressor_model(X_train, X_test, y_train, y_test, 100)
    #
    # mse_randomF = mean_squared_error(y_test, yhat_randomF)
    #
    # print 'randomF_rscore: ',randomF_rscore
    # print 'oob_score: ',oob_score
    # print 'mse_randomF: ', mse_randomF
    # '''get training score'''
    # yhat_train = rfr_model.predict(X_train)
    # print 'training r2_score: ',r2_score(y_train, yhat_train)
    #

    # '''save the model to a pickle file'''
    # dump_object_to_pickle(rfr_model, rfr_model_pickle_filename)
