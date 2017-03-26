'''Use survial model: '''

from sklearn.preprocessing import scale
from sklearn.utils import resample
# from matplotlib.colors import colorConverter
from lifelines import AalenAdditiveFitter
from sklearn.metrics import r2_score
import pickle
from lifelines.utils import k_fold_cross_validation
from lifelines import CoxPHFitter
from lifelines.datasets import load_regression_dataset
from lifelines.utils import k_fold_cross_validation


def aalen_aditive_model(df, target_col = 'Process_days', event = 'Event', coeff_pen = 0.5, smooth_pen = 0.1):
    '''creat an Aalen Additive Fitter instance that fits the regression model:
    with hazard(t)  = b_0(t) + b_1(t)*x_1 + ... + b_N(t)*x_N
    i.e., the hazard rate is a linear function of the covariates.
    Parameters
    df: Pandas dataframe.
    target_col: The y column.
    even_col: A column of 1 or 0 indicating if the event happened or not.
    coeff_pen = 0.1: Attach a L2 penalizer to the size of the coeffcients during regression. This improves
        stability of the estimates and controls for high correlation between covariates.  For example,
        this shrinks the absolute value of c_{i,t}. Recommended, even if a small value.
    Smoothing_penalizer = 0.1: Attach a L2 penalizer to difference between adjacent (over time) coefficents. For
        example, this shrinks the absolute value of c_{i,t} - c_{i,t+1}.

    Other built-in, unadjustable parameters:
    Intercept = False.  We suggest adding a column of 1 to model the baseline hazard.
    nn_cumulative_hazard = True:  In its True state, it forces the the negative hazard values to be zero
    Output: aaf instance fitted to df'''
    aaf = AalenAdditiveFitter(fit_intercept=True, coef_penalizer=coeff_pen, smoothing_penalizer=smooth_pen, nn_cumulative_hazard=True)
    aaf.fit(df, target_col, event_col=event)
    return aaf

'''use CoxPHFitter model'''

def Cox_model(df, target_col = 'Process_days', event = 'Event', coeff_pen = 0.5, smooth_pen = 0.1):
    '''creat aCoxPH instance
    Args:
    df: Pandas dataframe.
    target_col: The y column.
    even_col: A column of 1 or 0 indicating if the event happened or not.

    Other built-in, unadjustable parameters:
    Intercept = False.  We suggest adding a column of 1 to model the baseline hazard.
    nn_cumulative_hazard = True:  In its True state, it forces the the negative hazard values to be zero
    Output: aaf instance fitted to df'''
    coxf = CoxPHFitter()
    coxf.fit(df, target_col, event_col=event)
    return coxf
