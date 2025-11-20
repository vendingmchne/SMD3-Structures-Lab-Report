# -*- coding: utf-8 -*-
"""
Created on Tue Nov 11 19:08:24 2025

@author: raven
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sympy


###DATA INPUT
df = pd.read_excel("df input.xlsx")
x = df["Angle"]
yh = df["Horizontal Deflection"]
yv = df["Vertical Deflection"]

### REGRESSION TO SOLVE ROOTS

def regression(degree, x, y):
    Mx = np.zeros((degree + 1, degree + 1))
    vct = np.zeros((degree + 1))
    for i in range(degree + 1):
        for j in range(degree + 1):
            Mx[i, j] = np.sum(x**(i+j))
        vct[i] = np.sum(y * x**i)
    beta = np.linalg.solve(Mx, vct)
    return beta

xreg = np.linspace(0, 180, 1000)
beta_h = regression(4, x, yh)
beta_v = regression(4, x, yv)


yreg_h = np.zeros_like(xreg, dtype=float)
yreg_v = np.zeros_like(xreg, dtype=float)

for i in range(len(xreg)):
    for j in range(len(beta_h)):
        yreg_h[i] += beta_h[j] * xreg[i]**j
    for j in range(len(beta_v)):
        yreg_v[i] += beta_v[j] * xreg[i]**j

###SYMPY CONVERSION
z = sympy.symbols('z')
hexpr = 0
vexpr = 0
for i in range(len(beta_h)):
    hexpr += beta_h[i] * z**i
    vexpr += beta_v[i] * z**i
 
x
hdrv = sympy.diff(hexpr, z)   
vdrv = sympy.diff(vexpr, z)

hdrv_func = sympy.lambdify(z, hdrv, 'numpy')
vdrv_func = sympy.lambdify(z, vdrv, 'numpy')

hdrv_vals = hdrv_func(xreg)
vdrv_vals = vdrv_func(xreg)

h_roots = sympy.solve(hexpr, z)
vdrv_roots = sympy.solve(vdrv, z)

###PLOTS

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial']
fig, axs = plt.subplots(1, 2, figsize=(8, 3))
fig.tight_layout()
axs[0].plot(xreg, yreg_h)
axs[0].scatter(x, yh)
axs[0].set_title("Horizontal Deflection")
axs[0].set_ylabel("Deflection (mm)")

axs[1].plot(xreg, yreg_v)
axs[1].scatter(x, yv)
axs[1].set_title("Vertical Deflection")





      
h_rootsarr = []
vdrv_rootsarr = []

for i in range(len(h_roots)):
    r = complex(h_roots[i])     # convert sympy root → python complex
    rmag = abs(r)               # magnitude as float
    if i == 0 or rmag > 180:
        continue
    print(rmag)
    h_rootsarr.append(rmag)

for i in range(len(vdrv_roots)):
    r = complex(vdrv_roots[i])
    rmag = abs(r)
    if rmag > 180:
        continue
    print(rmag)
    vdrv_rootsarr.append(rmag)


for i in range(len(h_rootsarr)):
    hrootplotarr = np.full_like(yreg_h, h_rootsarr[i])
    axs[0].axvline(h_rootsarr[i], color="red", label = "Root of principal axis", ls = "dashed")
for i in range(len(vdrv_rootsarr)):
    vdrvrootplotarr = np.full_like(yreg_v, vdrv_rootsarr[i])
    axs[1].axvline(vdrv_rootsarr[i], color = "red", label = "Root of principal axis", ls = "dashed")    

print(np.round(h_rootsarr, 3))
print(np.round(vdrv_rootsarr, 3))