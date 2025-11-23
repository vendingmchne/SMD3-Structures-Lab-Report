# -*- coding: utf-8 -*-
"""
Created on Tue Nov 11 19:08:24 2025

@author: raven
"""
##Package import
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sympy


##Data input
df = pd.read_excel("df input.xlsx")
x = df["Angle"]
yHorz = df["Horizontal Deflection"]
yVert = df["Vertical Deflection"]

### REGRESSION TO SOLVE ROOTS

def regression(degree, x, y): #standard least squares method
    Mx = np.zeros((degree + 1, degree + 1))
    vct = np.zeros((degree + 1))
    for i in range(degree + 1):
        for j in range(degree + 1):
            Mx[i, j] = np.sum(x**(i+j))
        vct[i] = np.sum(y * x**i)
    beta = np.linalg.solve(Mx, vct)
    return beta

xRegression = np.linspace(0, 180, 1000)
betaH = regression(4, x, yHorz) #horz. regression beta vector
betaV = regression(4, x, yVert) #vert regression beta vector

##Regression array initialisation
yRegH = np.zeros_like(xRegression, dtype=float)
yRegV = np.zeros_like(xRegression, dtype=float)

for i in range(len(xRegression)):
    for j in range(len(betaH)):
        yRegH[i] += betaH[j] * xRegression[i]**j #populate values
    for j in range(len(betaV)):
        yRegV[i] += betaV[j] * xRegression[i]**j

###SYMPY CONVERSION
z = sympy.symbols('z')
symHorz = 0 #symbolic expression of horz and vert regressions
symVert = 0
for i in range(len(betaH)):
    symHorz += betaH[i] * z**i 
    symVert += betaV[i] * z**i
 
#take derivative of vertical 
symVertDrv = sympy.diff(symVert, z)

#setup symbol to array conversion
symHorzArray = sympy.lambdify(z, symHorz, 'numpy')
symVertDrvArray = sympy.lambdify(z, symVertDrv, 'numpy')

#symbol to array conversion
numHorz = symHorzArray(xRegression)
numVertDrv = symVertDrvArray(xRegression)

#find roots for plotting
horzRoots = sympy.solve(symHorz, z)
vertDrvRoots = sympy.solve(symVertDrv, z)

#Clean roots 
horzRootsArray = []
vertDrvRootsArray = []

for i in range(len(horzRoots)):
    r = complex(horzRoots[i])     # convert sympy root → python complex
    rmag = abs(r)               # magnitude as float - i term negligible
    if i == 0 or rmag > 180: #range of data
        continue
    horzRootsArray.append(rmag)

for i in range(len(vertDrvRoots)):
    r = complex(vertDrvRoots[i])
    rmag = abs(r)
    if rmag > 180:
        continue
    vertDrvRootsArray.append(rmag)
    

##Plots
plt.rcParams['font.family'] = 'sans-serif' #font setup
plt.rcParams['font.sans-serif'] = ['Arial'] 
fig, axs = plt.subplots(1, 2, figsize=(8, 3))
fig.tight_layout() #fig setup
#Horizontal [lot - scatter and regression
axs[0].plot(xRegression, yRegH) #plot regression
axs[0].scatter(x, yHorz) #plot empirical data
#horizontal plot labelling
axs[0].set_xlabel("Angle (deg)") 
axs[0].set_title("Horizontal Deflection")  
axs[0].set_ylabel("Deflection (mm)")

#Vertical plot - scatter and regression
axs[1].plot(xRegression, yRegV)
axs[1].scatter(x, yVert)
#vertical plot labelling - no need for deflection label
axs[1].set_title("Vertical Deflection")
axs[1].set_xlabel("Angle (deg)")

# Set tick label fontsize
axs[0].tick_params(axis='x', labelsize=6.5)
axs[0].tick_params(axis='y', labelsize=9)
axs[1].tick_params(axis='x', labelsize=6.5)
axs[1].tick_params(axis='y', labelsize=9)

#Define x ticks to set manual scale
x_increments = 10*np.arange(0, 19, 1)
axs[0].set_xticks(x_increments)
axs[1].set_xticks(x_increments)

#Roots plotting
for i in range(len(horzRootsArray)): #horizontal roots
    horzRootsPlotArray = np.full_like(yRegH, horzRootsArray[i])
    axs[0].axvline(horzRootsArray[i], color="red", label = "Root of principal axis", ls = "dashed")
for i in range(len(vertDrvRootsArray)): #vertical  derivative roots
    vertDrvRootsPlotArray = np.full_like(yRegV, vertDrvRootsArray[i])
    axs[1].axvline(vertDrvRootsArray[i], color = "red", label = "Root of principal axis", ls = "dashed")

#print statement for debug
print(np.round(horzRootsArray, 3))
print(np.round(vertDrvRootsArray, 3))

