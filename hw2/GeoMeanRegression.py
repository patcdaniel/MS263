# -*- coding: utf-8 -*-
"""
Compute the Geographic Mean regression
Created on Sun Feb 21 12:41:27 2016
@author: Patrick Daniel

From HW2:
Create a function that calculates the slope, and y-intercept, and confidence 
intervals (default 95%) for the slope of the geometric mean regression line, 
given two lists or arrays of numbers. See Equations 4 and 7 of Ricker (1984) 
for the slope and confidence intervals (here x and y are deviations from the 
mean of X and Y). In the docstring, describe how to use the function and the 
types of situations where you would a Type II regression like this.

"""
import numpy as np
from scipy import stats

def geoMeanRegression(xarray,yarray, confidence=.95):
    """ Calculate the Geometric Mean Regression from Ricker 1984

    Geometric mean regressions (GMR) is a symmetrical, robust, and scale
    invarriant regression. Confidence intervals are calculated from equation 7
    of Ricker 1984


    Args:
        xarray [array]: An array of data
        yarray [array]: An array of data
        confidence (optional[float]): alpha value for students t interval.
            default = .95

    Returns:
        r [float] = correlation coefficient
        slope [float] = slope of the GMR of Y on X(v)
        intercept [float] = y-intercept
        confidence_intervals [list] = plus and minus confidence intervals
    """
    mean_x = np.mean(xarray)
    mean_y = np.mean(yarray)
    CoVar_xy = sum( (xarray - mean_x)*(yarray - mean_y)) #Covariance of x and y S_xy
    coVar_sign = np.sign(CoVar_xy) #Store the sign of the covariance
    var_x = (sum((xarray - mean_x)**2)) / (len(xarray)-1) #Sample variance of x: S_xx
    var_y = (sum((yarray - mean_y)**2)) / (len(yarray)-1) #Sample variance of y: S_yy
    slope = coVar_sign * np.sqrt(var_y / var_x)
    r = coVar_sign / (np.sqrt(var_x) * np.sqrt(var_y)) #Sample correlation coefficient
    intercept = mean_y - mean_x * slope
    # Estimate Standard error w/ confidence
    df = len(xarray) + len(yarray) - 2 #N - 2
    t = stats.t.interval(confidence, df) #students confidence intervals
    s_v_squared = (slope ** 2 * (1 - r ** 2))/(df)
    prob = 2 * stats.t.sf(abs(t[0]), df)
    confidence_intervals = [np.sqrt(s_v_squared)*t[0],np.sqrt(s_v_squared)*t[1]]

    return r, slope, prob, intercept, confidence_intervals