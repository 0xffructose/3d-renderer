from PIL import Image,ImageDraw
from math import *
import numpy as np
from camera import Camera
import random
from cube import Cube
from rotations import *

"""

Method :
    First of all you have to subtract the camera position from selected 3D point. If you want to use rotations
    you must multiply the selected 3D point by each rotation matrice before multiplying by projection matrice. 
    
    Using Rotations - You have to multiply rotated point by perspective projection matrice.
    Not Using Rotations - You should multiply the 3D point by perspective projection matrice directly.

"""

width,height = 600,600
cx,cy = width/2,height/2

# Color dict. for simplify the point colors
colors = {"0":"WHITE","1":"PURPLE","2":"LIME","3":"YELLOW","4":"AQUA","5":"RED"}

image = Image.new('RGB',(width,height),color="BLACK")
draw = ImageDraw.Draw(image)

aspect_ratio = float(width/height)

# Camera object (You must create this object because projection matrice using this)
cam = Camera((0,0,-4),(0,0,0),fov=80)

# Perspective projection and scaling matrices
projection = np.array([(aspect_ratio * cam.f, 0, 0, 0),(0, cam.f, 0, 0),(0,0,-cam.znear-cam.zfar/cam.znear-cam.zfar,2*cam.zfar*cam.znear/cam.znear-cam.zfar),(0,0,1,0)])
scale = np.array([(50,0,0,0),(0,50,0,0),(0,0,50,0),(0,0,0,1)])

# TODO: Add textures

# You must add your objects into this list
objects = [Cube(pos=(0,0,0),color="0")]

points = []

for obj in objects:
    for vertice in obj.verts:
        # Converting the point to 1x4 matrice [x,y,z,w]
        px4 = [vertice[0],vertice[1],vertice[2],1]

        # Camera position subtraction
        
        px4[0] -= cam.pos[0]; px4[1] -= cam.pos[1]; px4[2] -= cam.pos[2];
        
        # Checking the camera rotation state (If camera position is in identity status then pass the rotation calcs.)
        if cam.rot != (0,0,0):
            print("Rotations calculating")
            # Rotations
            rotated = rotatey(px4,cam.rot[0])
            rotated = rotatex(rotated,cam.rot[1])
            rotated = rotatez(rotated,cam.rot[2])
            
            # Perspective projection and scaling
            px4 = np.matmul(rotated,projection)
            px4 = np.matmul(px4,scale)
            x,y = px4[0] * float(width) / (2.0 * px4[3]) + cx, px4[1] * float(height) / (2.0 * px4[3]) + cy
            points.append(("{}".format(objects.index(obj)),x,y))
        else:
            print("Rotations not calculating")
            px4 = np.matmul(px4,projection)
            px4 = np.matmul(px4,scale)
            # Clipping
            x,y = px4[0] * float(width) / (2.0 * px4[3]) + cx, px4[1] * float(height) / (2.0 * px4[3]) + cy
            points.append((obj.color,x,y))

for point in points:
    draw.ellipse([(int(point[1]-3),int(point[2]-3)),(int(point[1]+3),int(point[2]+3))],fill=colors[point[0]])

#region lines
"""
draw.line([(int(points[0][0]),int(points[0][1])),(int(points[1][0]),int(points[1][1]))],fill="WHITE")
draw.line([(int(points[2][0]),int(points[2][1])),(int(points[3][0]),int(points[3][1]))],fill="WHITE")
draw.line([(int(points[0][0]),int(points[0][1])),(int(points[6][0]),int(points[6][1]))],fill="WHITE")
draw.line([(int(points[1][0]),int(points[1][1])),(int(points[7][0]),int(points[7][1]))],fill="WHITE")
draw.line([(int(points[2][0]),int(points[2][1])),(int(points[4][0]),int(points[4][1]))],fill="WHITE")
draw.line([(int(points[3][0]),int(points[3][1])),(int(points[5][0]),int(points[5][1]))],fill="WHITE")
draw.line([(int(points[3][0]),int(points[3][1])),(int(points[1][0]),int(points[1][1]))],fill="WHITE")
draw.line([(int(points[0][0]),int(points[0][1])),(int(points[2][0]),int(points[2][1]))],fill="WHITE")
draw.line([(int(points[5][0]),int(points[5][1])),(int(points[7][0]),int(points[7][1]))],fill="WHITE")
draw.line([(int(points[6][0]),int(points[6][1])),(int(points[4][0]),int(points[4][1]))],fill="WHITE")
draw.line([(int(points[4][0]),int(points[4][1])),(int(points[5][0]),int(points[5][1]))],fill="WHITE")
draw.line([(int(points[6][0]),int(points[6][1])),(int(points[7][0]),int(points[7][1]))],fill="WHITE")
"""
#endregion

image.save("cube.png")