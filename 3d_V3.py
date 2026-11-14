import pygame
from math import *
import numpy as np
import file_reader as f
import random as r

WIDTH, HEIGHT = 200, 200
screen = pygame.display.set_mode((WIDTH*2, HEIGHT*2))
pygame.init()
clock = pygame.time.Clock()

class PLAYER:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.rotx = 0
        self.roty = 0
    def move(self):
        if pygame.key.get_pressed()[pygame.K_w]:
            self.x += sin(self.roty*pi/180)
            self.z += cos(self.roty*pi/180)
        if pygame.key.get_pressed()[pygame.K_s]:
            self.x -= sin(self.roty*pi/180)
            self.z -= cos(self.roty*pi/180)
        if pygame.key.get_pressed()[pygame.K_d]:
            self.x += cos(self.roty*pi/180)
            self.z -= sin(self.roty*pi/180)
        if pygame.key.get_pressed()[pygame.K_a]:
            self.x -= cos(self.roty*pi/180)
            self.z += sin(self.roty*pi/180)
        if pygame.key.get_pressed()[pygame.K_q]:
            self.y += 1
        if pygame.key.get_pressed()[pygame.K_e]:
            self.y -= 1
        if pygame.key.get_pressed()[pygame.K_UP]:
            self.rotx += 3
        if pygame.key.get_pressed()[pygame.K_DOWN]:
            self.rotx -= 3
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            self.roty += 3
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            self.roty -= 3
        if self.rotx < 0:
            self.rotx = 360
        if self.rotx > 360:
            self.rotx = 0
        if self.roty < 0:
            self.roty = 360
        if self.roty > 360:
            self.roty = 0
        
        

player = PLAYER(0, 0, 0)

def transform(px, py, pz):
    px = px - player.x
    py = py - player.y
    pz = pz - player.z
    point = np.array([px, py, pz])
    mroty = np.array([[cos(player.roty*pi/180), 0, sin(player.roty*pi/180)], [0, 1, 0], [-sin(player.roty*pi/180), 0, cos(player.roty*pi/180)]])
    mrotx = np.array([[1, 0, 0], [0, cos(player.rotx*pi/180), -sin(player.rotx*pi/180)], [0, sin(player.rotx*pi/180), cos(player.rotx*pi/180)]])
    point = np.matmul(point, mroty)
    point = np.matmul(point, mrotx)
    px = point[0]
    py = point[1]
    pz = point[2]
    if pz <= 0:
        return "behind"
    else:
        return px/pz*HEIGHT + WIDTH/2, py/pz*HEIGHT + HEIGHT/2

def cross_product(A, B, P):
    return (P[0] - A[0])*(B[1]-A[1]) - (P[1] - A[1])*(B[0] - A[0])

def is_inside(A, B, C, P): # check point P is in triangle ABC
    d1 = cross_product(A, B, P)
    d2 = cross_product(B, C, P)
    d3 = cross_product(C, A, P)
    if (d1 >= -1 and d2 >= -1 and d3 >= -1) or (d1 <= 1 and d2 <= 1 and d3 <= 1):
        return True
    else:
        return False

def dist(x1, y1, z1, x2, y2, z2):
    return sqrt((x1-x2)**2+(y1-y2)**2+(z1-z2)**2)

def sort_triangles(triangles, normals, player):
    distances  = []
    for tri in triangles:
        a = dist(*tri[0], player.x, player.y, player.z)
        b = dist(*tri[1], player.x, player.y, player.z)
        c = dist(*tri[2], player.x, player.y, player.z)
        distances.append((a+b+c)/3)
    paired = list(zip(distances, triangles, normals))
    paired.sort(key = lambda x: x[0], reverse = True)
    distances, triangles, normals = zip(*paired)
    distances = list(distances)
    triangles = list(triangles)
    normals = list(normals)
    return triangles, normals

def dot_product(a, b, c, d, e, f):
    return (a*d+b*e+c*f+1)/2


data = f.load_object(str(input("What file do you want to load?  ")), int(input("What size should it be scaled by?  ")))
triangles = data[0]
normals = data[1]
M_colour = (127, 127, 127)
light = [1, -1, 0]
mag = sqrt(light[0]**2+light[1]**2+light[2]**2)
light[0] = -light[0]/mag
light[1] /= mag             # dont flip y because normal is already upside down
light[2] = -light[2]/mag

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    clock.tick(60)
    player.move()
    Sorted = sort_triangles(triangles, normals, player)
    triangles = Sorted[0]
    normals = Sorted[1]
    screen.fill((255, 255, 255))
    c = 0
    for triangle in triangles:
        points = [transform(*triangle[0]), transform(*triangle[1]), transform(*triangle[2])]
        colour = (M_colour[0]-dot_product(light[0], light[1], light[2], normals[c][0], normals[c][1], normals[c][2])*M_colour[0], M_colour[1]-dot_product(light[0], light[1], light[2], normals[c][0], normals[c][1], normals[c][2])*M_colour[1], M_colour[2]-dot_product(light[0], light[1], light[2], normals[c][0], normals[c][1], normals[c][2])*M_colour[2]) # calculate lighting
        if "behind" in points:
            break
        x = [points[0][0], points[1][0], points[2][0]]
        y = [points[0][1], points[1][1], points[2][1]]
        AABB = max(min(x), 0), min(max(x), WIDTH), max(min(y), 0), min(max(y), HEIGHT)
        for x in range(int(AABB[1]-AABB[0])):
            for y in range(int(AABB[3]-AABB[2])):
                if is_inside(points[0], points[1], points[2], (x+AABB[0], y+AABB[2])):
                    screen.set_at(((x+AABB[0])*2, (y+AABB[2])*2), (colour))#((abs(int(normals[count][0]*255)), abs(int(normals[count][1]*255)), abs(int(normals[count][2]*255)))))
                    screen.set_at(((x+AABB[0])*2+1, (y+AABB[2])*2), (colour))#((abs(int(normals[count][0]*255)), abs(int(normals[count][1]*255)), abs(int(normals[count][2]*255)))))
                    screen.set_at(((x+AABB[0])*2+1, (y+AABB[2])*2+1), (colour))#((abs(int(normals[count][0]*255)), abs(int(normals[count][1]*255)), abs(int(normals[count][2]*255)))))
                    screen.set_at(((x+AABB[0])*2, (y+AABB[2])*2+1), (colour))#((abs(int(normals[count][0]*255)), abs(int(normals[count][1]*255)), abs(int(normals[count][2]*255)))))
        c += 1
    pygame.display.update()
