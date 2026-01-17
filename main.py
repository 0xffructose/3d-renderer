"""
Method :
    First of all you have to subtract the camera position from selected 3D point. If you want to use rotations
    you must multiply the selected 3D point by each rotation matrice before multiplying by projection matrice. 
    
    Using Rotations - You have to multiply rotated point by perspective projection matrice.
    Not Using Rotations - You should multiply the 3D point by perspective projection matrice directly.
"""

import pygame
import numpy as np

from src.scene.camera import Camera
from src.shapes import Cube
from src.rotations import *

from src.scene.scene import Scene
from src.mesh.mesh import Mesh

from src.mesh.parsers.obj_parser import ObjParser

pygame.init()

WIDTH , HEIGHT = 640 , 640
CX , CY = WIDTH//2 , HEIGHT//2

ASPECT_RATIO = float(WIDTH/HEIGHT)

CAMERA = Camera([0 , 0 , -4] , [0 , 0 , 0] , fov=80);

PROJECTION = np.array([
    (ASPECT_RATIO * CAMERA.f , 0 , 0 , 0) , 
    (0 , CAMERA.f , 0 , 0) ,
    (0 , 0 , -CAMERA.znear-CAMERA.zfar/CAMERA.znear-CAMERA.zfar , 2*CAMERA.zfar*CAMERA.znear/CAMERA.znear-CAMERA.zfar) , 
    (0 , 0 , 1 , 0)
])

SCALE = np.array([
    (50 , 0 , 0 , 0) , 
    (0 , 50 , 0 , 0) ,
    (0 , 0 , 50 , 0) ,
    (0 , 0 , 0 , 1)
])

CUBE = ObjParser().Parse("./cube.obj")
SPHERE = ObjParser().Parse("./sphere.obj")

SCENE = Scene([
    #Cube(pos=(0 , 0 , 0) , color="0")
    CUBE,
    SPHERE
])

POINTS = []

SCREEN = pygame.display.set_mode((WIDTH , HEIGHT)); pygame.display.set_caption("3D Renderer")
CLOCK = pygame.time.Clock()
RUNNING = True

DT = 0

while RUNNING:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                CAMERA.pos[0] -= .3
            elif event.key == pygame.K_RIGHT:
                CAMERA.pos[0] += .3
            elif event.key == pygame.K_UP:
                CAMERA.pos[2] -= .3
            elif event.key == pygame.K_DOWN:
                CAMERA.pos[2] += .3
            
            elif event.key == pygame.K_a:
                CAMERA.rot[0] -= .3
            elif event.key == pygame.K_d:
                CAMERA.rot[0] += .3
            elif event.key == pygame.K_w:
                CAMERA.rot[1] -= .3
            elif event.key == pygame.K_s:
                CAMERA.rot[1] += .3

            elif event.key == pygame.K_SPACE:
                CAMERA.pos[1] -= .3
            elif event.key == pygame.K_LSHIFT:
                CAMERA.pos[1] += .3

    SCREEN.fill("black")

    if (CAMERA.prev_pos != CAMERA.pos) or (CAMERA.prev_rot != CAMERA.rot):
        # print("Poses are not equal")
        POINTS = []

        for OBJ in SCENE.objects:
            for vertice in OBJ.verts:
                # Converting the point to 1x4 matrice [x,y,z,w]
                px4 = [float(vertice[0]),float(vertice[1]),float(vertice[2]),1]

                # Camera position subtraction
                
                px4[0] -= CAMERA.pos[0]; px4[1] -= CAMERA.pos[1]; px4[2] -= CAMERA.pos[2];
                
                # Checking the camera rotation state (If camera position is in identity status then pass the rotation calcs.)
                if CAMERA.rot != (0,0,0):
                    # print("Rotations calculating")
                    # Rotations
                    rotated = rotatey(px4 , CAMERA.rot[0])
                    rotated = rotatex(rotated , CAMERA.rot[1])
                    rotated = rotatez(rotated , CAMERA.rot[2])
                    
                    # Perspective projection and scaling
                    px4 = np.matmul(rotated , PROJECTION)
                    px4 = np.matmul(px4 , SCALE)
                    x , y = px4[0] * float(WIDTH) / (2.0 * px4[3]) + CX , px4[1] * float(HEIGHT) / (2.0 * px4[3]) + CY
                    POINTS.append(("{}".format(SCENE.objects.index(OBJ)),x,y))
                else:
                    # print("Rotations not calculating")
                    px4 = np.matmul(px4 , PROJECTION)
                    px4 = np.matmul(px4 , SCALE)
                    # Clipping
                    x,y = px4[0] * float(WIDTH) / (2.0 * px4[3]) + CX , px4[1] * float(HEIGHT) / (2.0 * px4[3]) + CY
                    POINTS.append((OBJ.color , x , y))
        CAMERA.Update()

    for POINT in POINTS:
        
        if POINT[1] < -1000 or POINT[1] > WIDTH + 1000 or POINT[2] < -1000 or POINT[2] > HEIGHT + 1000:
            continue

        pygame.draw.circle(
            SCREEN,
            (255 , 255 , 255),
            (int(POINT[1]) , int(POINT[2])) ,
            3
        )

    pygame.display.flip()
    DT = CLOCK.tick(60) / 1000

pygame.quit()