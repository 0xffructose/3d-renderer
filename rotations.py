import numpy as np
from math import cos,sin

def rotatex(point=(0,0,0,1),angle=0):
    rotationx = np.array([(1,0,0,0),(0,cos(angle),-sin(angle),0),(0,sin(angle),cos(angle),0),(0,0,0,1)]) 
    return np.matmul(point,rotationx)

def rotatey(point=(0,0,0,1),angle=0):
    rotationy = np.array([(cos(angle),0,sin(angle),0),(0,1,0,0),(-sin(angle),0,cos(angle),0),(0,0,0,1)]) 
    return np.matmul(point,rotationy)

def rotatez(point=(0,0,0,1),angle=0):
    rotationz = np.array([(cos(angle),-sin(angle),0,0),(sin(angle),cos(angle),0,0),(0,0,1,0),(0,0,0,1)]) 
    return np.matmul(point,rotationz)
