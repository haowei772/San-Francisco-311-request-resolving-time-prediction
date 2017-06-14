import pandas as pd
import numpy as np

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error
from EDA import days_to_hours
from sklearn.metrics import r2_score
import pickle


def LinearRegression_modle(X_train, X_test, y_train, y_test):
    '''
    Build a Linear regression model
    INPUT: dataframe and series of X_train, y_train, X_test, y_test from train_test_split
    OUTPUT: fitted model object, prediction based on X_test, test R2 score and MSE
    '''
    regr = LinearRegression(copy_X=True, fit_intercept=True, n_jobs=3, normalize=False)
    regr.fit(X_train, y_train)
    r_square = regr.score(X_test, y_test)
    yhat_linear = regr.predict(X_test)
    mse_linear = mean_squared_error(y_test, yhat_linear)
    return regr, yhat_linear, r_square, mse_linear

def RandomForestRegressor_model(X_train, X_test, y_train, y_test, estimators = 500):
    '''
    Build a random forest regressor model
    INPUT: dataframe and series of X_train, X_test, y_train, X_test from train_test_split, number of trees
    OUTPUT: fitted model object, prediction based on X_test, test R2 score and oob_score
    '''
    rfr = RandomForestRegressor(n_estimators=estimators, criterion='mse', n_jobs=-2, oob_score=True)
    rfr.fit(X_train, y_train)
    score = rfr.score(X_test,y_test)
    oob_score = rfr.oob_score_
    yhat = rfr.predict(X_test)
    return rfr, yhat, score, oob_score

'''GradientBoostingRegressor'''
def GradientBoostingRegressor_model(X_train, X_test, y_train, y_test, estimators = 200, learning_r = 0.1):
    '''
    Build a Gradient Boosting regressor model
    INPUT: dataframe and series of X_train, X_test, y_train, X_test from train_test_split, number of estimators, learning rate
    OUTPUT: fitted model object, prediction based on X_test, test R2 score
    '''
    gbr = GradientBoostingRegressor(n_estimators=estimators, max_depth=3, subsample=1, learning_rate=learning_r)
    gbr.fit(X_train, y_train)
    score = gbr.score(X_test,y_test)
    yhat = gbr.predict(X_test)
    return gbr, yhat, score
