# -*- coding: utf-8 -*-
"""
Created on Thu Feb 25 13:48:18 2016

@author: Patrick
"""

import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from matplotlib import pyplot as plt
from scipy import stats
import GeoMeanRegression
data = np.genfromtxt('WCOA/data/WCOA2013_hy1.csv',
              delimiter=',',
              skip_header=32,
              usemask=True,
              missing_values = '-999',
              filling_values = np.nan,
              invalid_raise=False)

# put some of the columns into variables with easily identifiable names
lat = data[:,10]
lon = data[:,11]
depth = data[:,12]
ctdprs = data[:,13]
ctdtmp = data[:,14]
ctdsal = data[:,15]
ctdoxy = data[:,17]
salinity = data[:,19]
oxygen = data[:,21]
silicate = data[:,23]
nitrate = data[:,25]
nitrite = data[:,27]
phosphate = data[:,29]
nh4 = data[:,31]

# np.maskedarrays need to be handeled
mask_good = ~nitrate.mask & ~oxygen.mask # An array of booleans to return where
nitrate_good = nitrate[mask_good]        # data is good at both values
nitrate_good = nitrate[mask_good]
oxygen_good = oxygen[mask_good]

# Oxygen vs Nitrate
r, slope, p, intercept, confidence_intervals = GeoMeanRegression.geoMeanRegression(nitrate_good,oxygen_good)
#Plot Regression
reg_x = np.linspace(0,45)
reg_y = (slope * reg_x) + intercept
textString1 = '*' * 30 + "\nSlope:" + str(slope) + "\nIntercept:" + str(intercept) + "\nslope confidence intervals:" + str(confidence_intervals) + "\nCorrelation Coefficient:"+ str(r) + "\np-value:" + str(p) + '\n' +'*'*30

# Latitude vs Temperature
# Get data between 150 and 200 meters
di = np.where((ctdprs > 150) & (ctdprs < 200))  # indices of data with pressure values between 150 and 200
tmp_subset = ctdtmp[di] # subset of temperature values corresponding to those indices
lat_subset = lat[di] # subset of lat

slope, intercept, r_value, p_value, std_err = stats.linregress(lat_subset,tmp_subset)
#Plot Regression
reg_x2 = np.linspace(36,50)
reg_y2 = (slope * reg_x2) + intercept
df = len(lat_subset) + len(tmp_subset) - 2
t = stats.t.cdf(.95,df)
slope_confidence_interval = [slope - t*std_err ,slope + t*std_err]
textString2 = '*' * 30 + "\nSlope:" + str(slope) + "\nIntercept:" + str(intercept) + "\nslope confidence intervals:" + str(slope_confidence_interval) + "\nCorrelation Coefficient:"+ str(r_value) + "\np-value:" + str(p_value) + '\n' +'*'*30

# Latitude vs Oxygen
# Get data between 150 and 200 meters
di = np.where((ctdprs > 150) & (ctdprs < 200))  # indices of data with pressure values between 150 and 200
oxy_subset = ctdoxy[di] # subset of temperature values corresponding to those indices
lat_subset = lat[di] # subset of lat

slope, intercept, r_value, p_value, std_err = stats.linregress(lat_subset,oxy_subset)
#Plot Regression
reg_x3 = np.linspace(36,50)
reg_y3 = (slope * reg_x3) + intercept
df = len(lat_subset) + len(oxy_subset) - 2
t = stats.t.cdf(.95,df)
slope_confidence_interval = [slope - t*std_err ,slope + t*std_err]
textString3 = '*' * 30 + "\nSlope:" + str(slope) + "\nIntercept:" + str(intercept) + "\nslope confidence intervals:" + str(slope_confidence_interval) + "\nCorrelation Coefficient:"+ str(r_value) + "\np-value:" + str(p_value) + '\n' +'*'*30

print "Fig. 1 Nitrate vs DO"
print textString1
print "Fig. 2 Latitude vs Temperature"
print textString2
print "Fig. 3 Latitude vs DO"
print textString3

fig, (ax1,ax2,ax3) = plt.subplots(3,1)
fig.subplots_adjust(hspace=.75)


ax1.plot(nitrate_good,oxygen_good,'.')
ax1.plot(reg_x,reg_y)
ax1.set_xlim([0,47])
ax1.set_title('Geometric Mean Regression of nitrate and oxygen',size=13)
ax1.set_ylabel('Dissolved Oxygen\n[$\mu$mol/kg]',size=13)
ax1.set_xlabel('Nitrate, [$\mu$mol/kg]',size=13)
# ax1.figtext(1.1 ,.5,textString1,size=14)


ax2.plot(lat_subset,tmp_subset,'.')
ax2.plot(reg_x2,reg_y2)
ax2.set_title("type I linear regression",size=13)
ax2.set_ylabel('Temperature, C',size=13)
ax2.set_xlabel('Latitude, degrees',size=13)
# ax2.text(ax2.get_xlim()[1]*1.01 ,ax2.get_ylim()[1]*.65,textString2,size=14)

ax3.plot(lat_subset,oxy_subset,'.')
ax3.plot(reg_x3,reg_y3)
ax3.set_title("Type I linear regression",size=13)
ax3.set_ylabel('Dissolved Oxygen\n$_mu$mol/kg',size=13)
ax3.set_xlabel('Latitude, degrees',size=13)
# ax3.text(ax3.get_xlim()[1]*1.01 ,ax3.get_ylim()[1]*.5,textString3,size=14)
plt.show()
