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


    '''Check if there is pickle files of dataframe and category dictionaries ready for load'''
    df_pickle_filename = '../data/df_tr.pickle'
    dict_pickle_filename = '../data/category_dict.pickle'
    filename_train = '../data/SF311_train.csv'

    df_tr, category_dictionaries = get_df_for_modeling(df_pickle_filename, dict_pickle_filename,filename_train)

    df_train, df_test = train_test_df_split(df_tr, test_size = 0.2, random_seed = 111)
    print 'df_train: ', len(df_train), ' df_test: ', len(df_test)

    '''Generate 100 cluster of 'Request Topic''''
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
