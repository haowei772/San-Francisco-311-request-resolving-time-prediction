from lifelines import AalenAdditiveFitter
from sklearn.metrics import r2_score
from SurvivalModel import aalen_aditive_model
from lifelines.utils import k_fold_cross_validation
from PremodelingProcess import train_vali_split, get_df_for_modeling, train_test_df_split, process_data_for_survival_model, dump_object_to_pickle

if __name__ == '__main__':
    '''Check if there is pickle files of dataframe and category dictionaries ready for load'''
    df_pickle_filename = '../data/df_tr.pickle'
    dict_pickle_filename = '../data/category_dict.pickle'
    aff_model_pickle_filename = '../results/aff_model.pickle'
    filename_train = '../data/SF311_train.csv'
    df, category_dictionaries = get_df_for_modeling(df_pickle_filename, dict_pickle_filename, filename_train)

    df_train, df_test = process_data_for_survival_model(df, test_size = 0.2, random_state = 222)
    print 'start training...'
    aaf_model = aalen_aditive_model(df_train, target_col = 'Process_days', event = 'Event', coeff_pen = 1, smooth_pen = 0.1)
    print 'start predicting...'
    yhat = aaf_model.predict_expectation(df_test)
    y_test = df_test['Process_days']
    aff_rscore2 = r2_score(y_test, yhat )
    print 'aff_rscore: ', aff_rscore2

    '''cross validation'''
    print 'start cross validation'
    cross_val_scores = k_fold_cross_validation(aaf_model, df_train, 'Process_days', event_col='Event', k=3)
    print cross_val_scores

    '''save the model to a pickle file'''
    dump_object_to_pickle(aff_model, aff_model_pickle_filename)

    # X_train, X_test, y_train, y_test = train_vali_split(df_tr, 'Process_days', test_size = 0.2, random_seed = 100)
    # print 'X_train: ', len(X_train)
    # print 'X_test: ', len(X_test)
    # gbr_model, yhat_Gboosting, Gboosting_rscore = GradientBoostingRegressor_model(X_train, X_test, y_train, y_test, estimators=200)
    # mse_Gboosting = mean_squared_error(y_test, yhat_Gboosting)
    #
    # print 'Gboosting_rscore: ',Gboosting_rscore
    # print 'mse_Gboosting: ', mse_Gboosting
    #
    # print 'Start k-fold cross validation'
    # cross_val_scores = cross_val_score(gbr_model, X_train, y_train, cv=3)
    # print 'cross_val_scores: ', cross_val_scores
