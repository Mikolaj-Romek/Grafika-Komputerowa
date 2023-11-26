import pygame
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import math
from time import time

sun_x = 0
sun_z = 0
sun_angle = 0
vertices = [
    [1, 1, 1],
    [-1, -1, 1],
    [-1, 1, -1],
    [1, -1, -1]
]

zoom = 5.0
rotation_x = 0
rotation_y = 0

color_enabled = True

def draw_tetrahedron(v1, v2, v3, v4):
    glBegin(GL_TRIANGLES)

    if color_enabled:
        glColor3fv((1.0, 0.0, 0.0))  # Red
        glVertex3fv(v1)
        glVertex3fv(v2)
        glVertex3fv(v3)

        glColor3fv((0.0, 1.0, 0.0))  # Green
        glVertex3fv(v1)
        glVertex3fv(v2)
        glVertex3fv(v4)

        glColor3fv((0.0, 0.0, 1.0))  # Blue
        glVertex3fv(v1)
        glVertex3fv(v3)
        glVertex3fv(v4)

        glColor3fv((1.0, 1.0, 1.0))  # White
        glVertex3fv(v2)
        glVertex3fv(v3)
        glVertex3fv(v4)
    else:
        # If color is disabled, draw using a single color
        glColor3fv((1.0, 1.0, 1.0))  # White
        glVertex3fv(v1)
        glVertex3fv(v2)
        glVertex3fv(v3)

        glVertex3fv(v1)
        glVertex3fv(v2)
        glVertex3fv(v4)

        glVertex3fv(v1)
        glVertex3fv(v3)
        glVertex3fv(v4)

        glVertex3fv(v2)
        glVertex3fv(v3)
        glVertex3fv(v4)

    glEnd()

def subdivide(v1, v2, v3, v4, depth):
    if depth > 0:
        v12 = [(v1[i] + v2[i]) / 2 for i in range(3)]
        v13 = [(v1[i] + v3[i]) / 2 for i in range(3)]
        v14 = [(v1[i] + v4[i]) / 2 for i in range(3)]
        v23 = [(v2[i] + v3[i]) / 2 for i in range(3)]
        v24 = [(v2[i] + v4[i]) / 2 for i in range(3)]
        v34 = [(v3[i] + v4[i]) / 2 for i in range(3)]

        subdivide(v1, v12, v13, v14, depth - 1)
        subdivide(v12, v2, v23, v24, depth - 1)
        subdivide(v13, v23, v3, v34, depth - 1)
        subdivide(v14, v24, v34, v4, depth - 1)
    else:
        draw_tetrahedron(v1, v2, v3, v4)

def sierpinski_pyramid(vertices, depth):
    subdivide(vertices[0], vertices[1], vertices[2], vertices[3], depth)


def setup_lighting():
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)  # Directional Light
    glEnable(GL_LIGHT1)  # Point Light

    # Directional light properties
    glLightfv(GL_LIGHT0, GL_POSITION, (0, 1, 1, 0))  # Directional light from above
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (1, 1, 1, 1))  # Diffuse component (white)
    glLightfv(GL_LIGHT0, GL_SPECULAR, (1, 1, 1, 1))  # Specular component (white)

    # Point light properties
    glLightfv(GL_LIGHT1, GL_POSITION, (2, 2, 2, 1))  # Point light position
    glLightfv(GL_LIGHT1, GL_DIFFUSE, (1, 1, 1, 1))  # Diffuse component (white)
    glLightfv(GL_LIGHT1, GL_SPECULAR, (1, 1, 1, 1))  # Specular component (white)


def draw_sphere(radius, slices, stacks):
    sphere = gluNewQuadric()
    gluQuadricTexture(sphere, GL_TRUE)
    gluQuadricNormals(sphere, GLU_SMOOTH)
    gluSphere(sphere, radius, slices, stacks)


def setup_sunlight():
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)  # Sunlight as the source of light

    sun_position = [sun_x, 2, sun_z, 1.0]  # Define the position of the sun
    glLightfv(GL_LIGHT0, GL_POSITION, sun_position)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (1.0, 1.0, 1.0, 1.0))  # Set the diffuse component to white
    glLightfv(GL_LIGHT0, GL_SPECULAR, (1.0, 1.0, 1.0, 1.0))  # Set the specular component to white


def draw_sphere_light(radius, slices, stacks):
    glPushMatrix()
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT2)

    # Position the light source within the sphere
    glLightfv(GL_LIGHT2, GL_POSITION, (0, 0, 0, 1))
    glLightfv(GL_LIGHT2, GL_DIFFUSE, (1.0, 1.0, 1.0, 0.0))  # White light

    glColor3f(1.0, 1.0, 0.0)  # Yellow sphere representing the sun
    gluSphere(gluNewQuadric(), radius, slices, stacks)

    glPopMatrix()
def main():
    global zoom, rotation_x, rotation_y, color_enabled, sun_angle

    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, pygame.OPENGL | pygame.DOUBLEBUF)
    glEnable(GL_DEPTH_TEST)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)

    glTranslatef(0.0, 0.0, -15)  # Position adjusted to stand on the ground


    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    glTranslatef(0.0, 0.0, 1.0)
                if event.button == 5:
                    glTranslatef(0.0, 0.0, -1.0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    color_enabled = not color_enabled  # Toggle color display

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            glTranslatef(0.1, 0, 0)
        if keys[pygame.K_RIGHT]:
            glTranslatef(-0.1, 0, 0)
        if keys[pygame.K_UP]:
            glTranslatef(0, -0.1, 0)
        if keys[pygame.K_DOWN]:
            glTranslatef(0, 0.1, 0)





        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glRotatef(0.1, 1, 1, 1)
        sierpinski_pyramid(vertices, 3)  # Adjust the recursion level here

        distance = 3.0  # Distance from the center


        #sun_angle = (time() * 10) % 360  # Adjust the speed of rotation as needed
        #sun_x = 5 * math.cos(math.radians(sun_angle))
        #sun_z = 5 * math.sin(math.radians(sun_angle))

        glPushMatrix()
        #glTranslate(sun_x, sun_z, 0)  # Translate sphere position
        #draw_sphere_light(0.3, 30, 30)  # Adjust sphere parameters here
        glPopMatrix()





        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()