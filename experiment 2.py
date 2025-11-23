# -*- coding: utf-8 -*-
"""
Created on Sun Nov 16 22:59:30 2025

@author: raven
"""

##Package import
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

##Data import
df = pd.read_excel("exp 2 df input.xlsx")

##Params
#Geometry
width = 0.0251 #m
thickness = 0.0034 #m
R_inner = 0.2905/2 #m
R_med = R_inner + thickness / 2 #m
R_outer = R_inner + thickness #m
#Theoretical Deflection 
P = df["Weight (N)"] #load - independent var.
Ix = width*thickness**3/12 #Area MOI for rectangle
E = 210 * 10**9
slopeh_theory = 2 * R_med**3 / (E * Ix) #Castigliano's Theorem
slopev_theory = np.pi * R_med**3 / (E * Ix)

##Arrays
#Theoretical arrays
P_theory = np.linspace(0, 12, 100) 
dh_theory = P_theory * slopeh_theory #Lines for theoretical deflection vs load
dv_theory = P_theory * slopev_theory
#Experimental Arrays
dh_exp = df["Mean H_D (m)"]
dv_exp = df["Mean V_D (m)"]

##Error Calculations

#Theory error
def relerr(error, value):
    return error/value 

err_width = 0.00001 #resolution
relerr_width = relerr(err_width, width)

err_thickness = 0.00001 #resolution
relerr_thickness = relerr(err_thickness, thickness)

err_Rmed = 0.00051 #resolution of micrometer and ruler
relerr_Rmed = relerr(err_Rmed, R_med)  

#Assume no error in weight, Young modulus
relerr_I = relerr_width + 3*relerr_thickness #cubic terms triple error

relerr_d = 3*relerr_Rmed + relerr_I

#Scale slopes for error 
err_dh_theory = dh_theory * relerr_d 
err_dv_theory = dv_theory * relerr_d

##Linear regression
#parameters
xmean = np.average(P) 
yhmean = np.average(dh_exp)
yvmean = np.average(dv_exp)
#initialise sums for both regression lines
sumxyh = 0
sumxyv = 0
sumyh = 0
sumyv = 0
sumxsq = 0
for i in range(len(P)): #add to each term in regression formula
    sumxyh += (P[i] - xmean) * (dh_exp[i] - yhmean) 
    sumxyv += (P[i] - xmean) * (dv_exp[i] - yvmean)
    sumxsq += (P[i] - xmean)**2

#regression equation calculated params.
regslopeh = sumxyh / sumxsq #
regslopev = sumxyv / sumxsq
intcpth = yhmean - regslopeh * xmean
intcptv = yvmean - regslopev * xmean

#R squared calculation
SSresh = 0
SSresv = 0
sumysqh = 0
sumysqv = 0
for i in range(len(P)):
    SSresh += (dh_exp - (intcpth + regslopeh * P))**2
    SSresv += (dv_exp - (intcptv + regslopev * P))**2
    sumysqh += (dh_exp - yhmean)**2
    sumysqv += (dv_exp - yvmean)**2

rsqh = 1 - SSresh/sumysqh
rsqv = 1 - SSresv/sumysqv

##Plots
#set up figure
fig, axs = plt.subplots(ncols = 2, figsize = (10, 3)) #side by side

#set up font
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial']

#Horizontal plot labelling
axs[0].set_title('Horizontal Deflection')
axs[0].set_xlabel('Load (P)')
axs[0].set_ylabel('Deflection (m)')
#Vertical plot labelling
axs[1].set_title('Vertical Deflection')
axs[1].set_xlabel('Load (P)')
axs[1].set_ylabel('Deflection (m)')

#Theoretical lines 
axs[0].plot(P_theory, dh_theory, lw = 1, c = "red", label = "Theory")
axs[1].plot(P_theory, dv_theory, lw = 1, c = "red", label = "Theory")
#Theoretical Error Plots
#horizontal
axs[0].plot(P_theory, dh_theory + err_dh_theory, lw = 0.5, c = "black", label = "Theoretical error upper bound")
axs[0].plot(P_theory, dh_theory - err_dh_theory, lw = 0.5, c = "black", label = "Theoretical error lower bound")
#vertical
axs[1].plot(P_theory, dv_theory + err_dv_theory, lw = 0.5, c = "black", label = "Theoretical error upper bound")
axs[1].plot(P_theory, dv_theory - err_dv_theory, lw = 0.5, c = "black", label = "Theoretical error lower bound")
#Experimental error bars
#horizontal
axs[0].scatter(P, dh_exp)
axs[0].errorbar(P, dh_exp, yerr = df["Error in H_D (m)"], fmt = "o", color = "#008800", ecolor = "#0000FF")
#vertical
axs[1].scatter(P, dv_exp)
axs[1].errorbar(P, dv_exp, yerr = df["Error in V_D (m)"], fmt = "o", color = "#008800", ecolor = "#0000FF")
#Experimental Regression Plots
axs[0].plot(P, (intcpth + regslopeh * P), c = "black", label = "Regression slope", linestyle = "dashed")
axs[1].plot(P, (intcptv + regslopev * P), c = "black", label = "Regression slope", linestyle = "dashed")
#Legends
axs[0].legend(fontsize = 6)
axs[1].legend(fontsize = 6) 

plt.show()

print("R^2 for horz: ", rsqh, "R^2 for vert: ", rsqv)
print(Ix)

