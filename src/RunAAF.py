from lifelines import AalenAdditiveFitter
from sklearn.metrics import r2_score
from SurvivalModel import aalen_additive_model
aalen_additive_model
from lifelines.utils import k_fold_cross_validation
from PremodelingProcess import train_vali_split, get_df_for_modeling, train_test_df_split, process_data_for_survival_model, dump_object_to_pickle

if __name__ == '__main__':
    '''Check if there is pickle files of dataframe and category dictionaries ready for load'''
    df_pickle_filename = '../data/df_tr.pickle'
    dict_pickle_filename = '../data/category_dict.pickle'
    aff_model_pickle_filename = '../data/aff_model.pickle'

    filename_train = '../data/SF311_train.csv'
    df, category_dictionaries = get_df_for_modeling(df_pickle_filename, dict_pickle_filename, filename_train)

    '''simplify the the model'''
    kept_list = ['Responsible Agency', 'Category','Request Topic', 'Neighborhood','Supervisor District', 'Process_days', 'Weekend', 'Holiday', 'Open_Time']
    df = df[kept_list]
    # limit = int(0.8*len(df))
    # '''only try the most recent 1/4 of data'''
    # df = df[limit:]
    print len(df)
    df_train, df_test = process_data_for_survival_model(df, test_size = 0.2, random_state = 222)
    print 'start training... training data: ', len(df_train)
    aaf_model = aalen_additive_model(df_train, target_col = 'Process_days', event = 'Event', coeff_pen = 1, smooth_pen = 0.1)
    dump_object_to_pickle(aaf_model, aff_model_pickle_filename)

    print 'start predicting... test data: ', len(df_test)
    yhat = aaf_model.predict_expectation(df_test)
    y_test = df_test['Process_days']
    aff_rscore2 = r2_score(y_test, yhat )
    print 'aff_rscore: ', aff_rscore2

    '''cross validation, this is using the model trained from df_train, so it's just perform on the training data not test or validation set'''
    print 'start cross validation'
    cross_val_scores = k_fold_cross_validation(aaf_model, df_train, 'Process_days', event_col='Event', k=3)
    print cross_val_scores
