import pandas as pd
import numpy as np

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error
from EDA import days_to_hours
from sklearn.metrics import r2_score
import pickle
# from matplotlib.colors import colorConverter



'''$$$$$$$$$$$$$$$$$$$$ Start modeling $$$$$$$$$$$$$$$$$$$$'''
'''linear regression model'''
def LinearRegression_modle(X_train, X_test, y_train, y_test):
    regr = LinearRegression(copy_X=True, fit_intercept=True, n_jobs=3, normalize=False)

    regr.fit(X_train, y_train)
    r_square = regr.score(X_test, y_test)

    yhat_linear = regr.predict(X_test)
    mse_linear = mean_squared_error(y_test, yhat_linear)

    return regr, yhat_linear, r_square, mse_linear



'''RandomForest regressor model'''
'''RandomForestRegressor'''
def RandomForestRegressor_model(X_train, X_test, y_train, y_test, estimators = 500):
    rfr = RandomForestRegressor(n_estimators=estimators, criterion='mse', n_jobs=-2, oob_score=True)
    '''other parameters:
    RandomForestClassifier(n_estimators=10, criterion='mse', max_depth=None, min_samples_split=2,
    min_samples_leaf=1, min_weight_fraction_leaf=0.0, max_features='auto', max_leaf_nodes=None,
    min_impurity_split=1e-07, bootstrap=True, oob_score=False, n_jobs=1, random_state=None,
    verbose=0, warm_start=False)
    '''
    rfr.fit(X_train, y_train)
    '''r_square'''
    score = rfr.score(X_test,y_test)
    oob_score = rfr.oob_score_
    yhat = rfr.predict(X_test)
    return rfr, yhat, score, oob_score

'''Gradient boosting model'''


'''GradientBoostingRegressor'''
def GradientBoostingRegressor_model(X_train, X_test, y_train, y_test, estimators = 200, learning_r = 0.1):
    gbr = GradientBoostingRegressor(n_estimators=estimators, max_depth=3, subsample=1, learning_rate=learning_r)
    '''other parameter:
    GradientBoostingRegressor(loss='ls', learning_rate=0.1, n_estimators=100, subsample=1.0,
    criterion='friedman_mse', min_samples_split=2, min_samples_leaf=1, min_weight_fraction_leaf=0.0,
    max_depth=3, min_impurity_split=1e-07, init=None, random_state=None, max_features=None,
    alpha=0.9, verbose=0, max_leaf_nodes=None, warm_start=False, presort='auto')
    '''
    gbr.fit(X_train, y_train)
    '''r_square'''
    score = gbr.score(X_test,y_test)
    yhat = gbr.predict(X_test)
    return gbr, yhat, score

# def plot_importance(model, X, max_features=10):
#     '''Plot feature importance'''
#     feature_importance = model.feature_importances_
#     '''make importances relative to max importance'''
#     feature_importance = 100.0 * (feature_importance / feature_importance.max())
#     sorted_idx = np.argsort(feature_importance)
#     pos = np.arange(sorted_idx.shape[0]) + .5
#
#     '''Show only top features'''
#     pos = pos[-max_features:]
#     feature_importance = (feature_importance[sorted_idx])[-max_features:]
#     feature_names = (X.columns[sorted_idx])[-max_features:]
#
#     plt.figure(figsize = (12,8))
#     plt.barh(pos, feature_importance, align='center', color = 'g')
#     plt.yticks(pos, feature_names)
#     plt.xlabel('Relative Importance')
#     plt.title('Feature Importance')
#     return feature_importance

'''Will use KNN to impute the neighborhood, but before doing it need to split the data into train-valid and test set'''
'''Because KNN will use information from the whole dataset, lead to a data leakage'''
'''Do a 80-20% train-test split on dataframe'''
# np.random.seed(seed = 111)
# df_fill['Flag'] = np.random.random(size = len(df_fill)) >=0.8
# df_train = df_fill[~df_fill['Flag']]
# df_test = df_fill[df_fill['Flag']]



'''$$$$$$$$$$$$$$$$$$$$ End modeling $$$$$$$$$$$$$$$$$$$$'''
