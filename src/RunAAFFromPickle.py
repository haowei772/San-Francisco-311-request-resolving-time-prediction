from lifelines import AalenAdditiveFitter
from sklearn.metrics import r2_score
from SurvivalModel import aalen_additive_model
aalen_additive_model
from lifelines.utils import k_fold_cross_validation
from PremodelingProcess import train_vali_split, get_df_for_modeling, train_test_df_split, process_data_for_survival_model, dump_object_to_pickle, load_object_from_pickle

if __name__ == '__main__':

    '''Check if there is pickle files of dataframe and category dictionaries ready for load'''
    df_pickle_filename = '../data/df_tr.pickle'
    dict_pickle_filename = '../data/category_dict.pickle'
    aff_model_pickle_filename = '../data/aff_model.pickle'

    filename_train = '../data/SF311_train.csv'
    df, category_dictionaries = get_df_for_modeling(df_pickle_filename, dict_pickle_filename, filename_train)

    '''simplify the the model'''
    kept_list = ['Responsible Agency', 'Request Type', 'Neighborhood', 'Process_days',  'Opened_Int']
    df = df[kept_list]
    limit = int(0.8*len(df))
    '''only try the most recent 1/4 of data'''
    df = df[limit:]
    print len(df)
    df_train, df_test = process_data_for_survival_model(df, test_size = 0.2, random_state = 222)

    # aff_model_pickle_filename = '../data/aff_model.pickle'
    aaf_model = load_object_from_pickle(aff_model_pickle_filename)
    print 'done with loading pickle'
    length = len(df_test)
    print 'start predicting... test data: ', length
    sets = 4
    aff_rscores =[]
    for i in range(sets-1):
        step = int(length/sets)
        start = int(i*step)
        print start, step
        df_test1 = df_test[start:(start+step)]
        len(df_test1)
        yhat = aaf_model.predict_expectation(df_test1)
        y_test = df_test1['Process_days']
        print yhat.shape, y_test.shape
        score = r2_score(y_test, yhat )
        print 'score: ', score
        aff_rscores.append( score)

    print 'aff_rscores: ', aff_rscores

    '''cross validation, this is using the model trained from df_train, so it's just perform on the training data not test or validation set'''
    print 'start cross validation'
    cross_val_scores = k_fold_cross_validation(aaf_model, df_train, 'Process_days', event_col='Event', k=3)
    print cross_val_scores

    # '''save the model to a pickle file'''
    # dump_object_to_pickle(aff_model, aff_model_pickle_filename)
    # print 'done'

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
