from MachineLearningModel import GradientBoostingRegressor_model
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
from PremodelingProcess import dump_object_to_pickle, train_vali_split, get_df_for_modeling

from sklearn.model_selection import cross_val_score


if __name__ == '__main__':
    '''Check if there is pickle files of dataframe and category dictionaries ready for load'''
    df_pickle_filename = '../data/df_tr.pickle'
    dict_pickle_filename = '../data/category_dict.pickle'
    gbr_model_pickle_filename = '../results/gbr_model.pickle'
    filename_train = '../data/SF311_train.csv'
    df_tr, category_dictionaries = get_df_for_modeling(df_pickle_filename, dict_pickle_filename, filename_train)

    '''simplify the the model'''
    print 'simplified model'
    kept_list = ['Responsible Agency', 'Supervisor District', 'Category','Request Type', 'Neighborhood', 'Process_days',  'Opened_Int']
    df_tr = df_tr[kept_list]

    X_train, X_test, y_train, y_test = train_vali_split(df_tr, 'Process_days', test_size = 0.2, random_seed = 100)

    print 'X_train: ', len(X_train)
    print 'X_test: ', len(X_test)
    gbr_model, yhat_Gboosting, Gboosting_rscore = GradientBoostingRegressor_model(X_train, X_test, y_train, y_test, estimators=400, learning_r = 0.05)
    mse_Gboosting = mean_squared_error(y_test, yhat_Gboosting)

    print 'Gboosting_rscore: ',Gboosting_rscore
    print 'mse_Gboosting: ', mse_Gboosting

    print 'Start k-fold cross validation'
    cross_val_scores = cross_val_score(gbr_model, X_train, y_train, cv=5)
    print 'cross_val_scores: ', cross_val_scores

    # '''save the model to a pickle file'''
    # dump_object_to_pickle(gbr_model, gbr_model_pickle_filename)
