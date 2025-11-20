# -*- coding: utf-8 -*-
"""
Created on Tue Nov 11 17:02:18 2025

@author: raven
"""

import numpy as np


#Parameters
L = 24.97
H = 27.01
T = 3.51

err = 0.01
err_T = 0.11

#Areas
A1 = L * T
A2 = T * (H - T)
##Centroid
#Length Leg Centroid
zg_L  = L/2
yg_L = T/2
#Height Leg Centroid
zg_H = T/2
yg_H = T + (H - T)/2

#Total Centroids
zg = (A1 * zg_L + A2 * zg_H) / (A1 + A2)
yg = (A1 * yg_L + A2 * yg_H) / (A1 + A2)


##Moments of Inertia 
Iz = L*T**3/12 + A1*(yg_L-yg)**2 + T*(H-T)**3/12 + A2*(yg_H - yg)**2
Iy = T*L**3/12 + A1*(zg_L - zg)**2 + (H-T)**3/12 + A2*(zg_H - zg)**2
Iyz = A1*(yg_L-yg)*(zg_L-zg) + A2*(yg_H-yg)*(zg_H-zg)


##Principal Axis
principal_angle = np.degrees(np.arctan(-2*Iyz/(Iz - Iy))/2)

##Image Moments of Inertia
Iu = (Iz + Iy)/2 + np.sqrt(((Iz-Iy)/2)**2+Iyz**2)
Iv = (Iz + Iy)/2 - np.sqrt(((Iz-Iy)/2)**2+Iyz**2)


print("Dimensions: Height  = ", H, "mm, Length = ", L, "mm, Thickness = ", T, "mm.")
print("Centroid: z = ", np.round(zg, 2), "mm, y = ", np.round(yg, 2), "mm")
print("Moments of Inertia: Iz = ", np.round(Iz, 3), "mm^4, Iy = ", np.round(Iy, 3), "mm^4, Iyz = ", np.round(Iyz, 3), "mm^4")
print("Angle of Principal Axes: ", np.round(principal_angle, 3), "deg")
print("Image moments of Inertia: \n Iu ", np.round(Iu, 3), "mm^4, \n Iv: ", Iv, "mm^4")