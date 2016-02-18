# -*- coding: utf-8 -*-
"""
Adding a line
Created on Sat Feb  6 10:37:27 2016
@author: Patrick (pdaniel@mlml.calstate.edu)
"""
from numpy import asarray,mean,std,sqrt
from scipy import stats
import random
def z_score(dataArray):
    """
    Compute the z_score of a an list of numbers
    return numpy.ndarray of z score values
    """
    dataArrayNp = asarray(dataArray) # Convert list to an np.ndarray
    return (dataArrayNp - mean(dataArrayNp)) / std(dataArrayNp) #Use biased or unbiased STD?

def confidence_t(dataArray,confidence=.95):
    """
    Returns an list with the range of the true mean at a defined confidence interval.
    
    Keyword arguments:
    dataArray -- Any list of int or float type
    confidence -- a decimal speciffying the confidence intervals (default - .95)
    """
    
    confidence = confidence + ((1 - confidence) / 2) # for a 95% confidence interval, 
    # for stats.t.ppf() use .975 for q for 95% confidence
    # Since each side is symetrical, use the negative value for the lower bound.
    lower_bound = mean(dataArray) - stats.t.ppf(confidence,len(dataArray)) * (std(dataArray)/sqrt(len(dataArray)))
    upper_bound = mean(dataArray) + stats.t.ppf(confidence,len(dataArray)) * (std(dataArray)/sqrt(len(dataArray)))
    return [lower_bound, upper_bound, confidence]

def confidence_chi(dataArray, confidence = .95):
    """
    Returns an list with the confidence intervals of the varience.
    Keyword arguments:
    dataArray -- Any list of int or float type
    confidence -- a decimal speciffying the confidence intervals (default - .95)
    """
    confidence = (1 - confidence) / 2 # for a 95% confidence interval, .025 and .975 are the upper and lower limits, for chi, these are asymmetrical
    df = len(dataArray)
    upper_bound = ((df-1) * (std(dataArray)**2)) / (stats.chi2.ppf(confidence, df))
    lower_bound = ((df-1) * (std(dataArray)**2)) / (stats.chi2.ppf(1.0 - confidence,df))
    return [lower_bound, upper_bound, confidence]
    
def main():
    # Test case
    a = random.sample(xrange(10),6)
    print "The z-scores for", a, "are:", z_score(a)
    print "Chi-square confidence values:", confidence_chi(a)[0], ":", confidence_chi(a)[1]
    print "T confidence values:", confidence_t(a)[0], ":", confidence_t(a)[1]

if __name__ == "__main__":
    main()
