
import MachineLearningModel
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import EDA
import PremodelingProcess
import DataCleaning
from PremodelingProcess import load_object_from_pickle, dump_object_to_pickle
import os

if __name__ == '__main__':
    '''Check if there is pickle files of dataframe and category dictionaries ready for load'''
    df_pickle_filename = '../data/df_tr.pickle'
    dict_pickle_filename = '../data/category_dict.pickle'
    if os.path.exists(df_pickle_filename) and os.path.exists(dict_pickle_filename):
        '''if os.path.isfile(filename): also works'''
        df_tr = DataCleaning.load_object_from_pickle(df_pickle_filename)
        print 'get df from pickle'
        category_dictionaries = PremodelingProcess.load_object_from_pickle(dict_pickle_filename)
    else:
        '''Read data from train csv file'''
        #folder = '/Users/haowei/Documents/GN/Capstone/Capstone-project/data/'
        filename_train = '../data/SF311_train.csv'

        df_tr = EDA.get_prep_data(filename_train)
        df_tr, category_dictionaries = PremodelingProcess.preprocess_data(df_tr)
        dump_object_to_pickle(df_tr,df_pickle_filename)
        dump_object_to_pickle(category_dictionaries, dict_pickle_filename)

    X_train, X_test, y_train, y_test = PremodelingProcess.train_vali_split(df_tr, 'Process_days', test_size = 0.3, random_seed = 100)
    '''linear regression model'''
    regr, yhat_linear, r_square, mse_linear = MachineLearningModel.LinearRegression_modle(X_train, X_test, y_train, y_test)

    print 'MSE Linear: ', mse_linear
    print 'r_square', r_square
