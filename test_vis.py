"""This script shows an example of using the PyWavefront module."""
import ctypes
import os
import sys

sys.path.append('..')

import pyglet
from pyglet.gl import *

from pywavefront import visualization
from pyglet.window import key
import pywavefront
import cv2

# Create absolute path from this module
file_abspath = os.path.join(os.path.dirname(__file__), './checkpoints/FaceReconTorch/results/epoch_20_000000/badLightingWoman.obj')

rotation_x = 0
rotation_y = 0
direction_x = 1
direction_y = 1
meshes = pywavefront.Wavefront(file_abspath)
window = pyglet.window.Window(resizable=True)
keys = pyglet.window.key.KeyStateHandler()
lightfv = ctypes.c_float * 4


@window.event
def on_resize(width, height):
    viewport_width, viewport_height = window.get_framebuffer_size()
    glViewport(0, 0, viewport_width, viewport_height)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(90., float(width)/height, 1., 100.)
    glMatrixMode(GL_MODELVIEW)
    return True


@window.event
def on_draw():
    window.clear()
    glLoadIdentity()

    glLightfv(GL_LIGHT0, GL_POSITION, lightfv(-1.0, 1.0, 1.0, 0.0))
    glEnable(GL_LIGHT0)

    glTranslated(0.0, 0.0, -3.0)
    # glRotatef(rotation, 0.0, 1.0, 0.0)
    # glRotatef(-25.0, 1.0, 0.0, 0.0)
    # glRotatef(45.0, 0.0, 0.0, 1.0)
    glRotatef(rotation_x, 0.0, 1.0, 0.0)
    glRotatef(rotation_y, 1.0, 0.0, 0.0)
    glRotatef(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_LIGHTING)

    visualization.draw(meshes)

# @window.event
# def on_key_press(symbol, modifiers):
#     global rotation_x
#     global rotation_y
#     print(f"{symbol} {modifiers}")
#     print(f"{key.UP} {key.DOWN} {key.LEFT} {key.RIGHT}")
#     if symbol == key.UP:
#         rotation_y += 1
#     elif symbol == key.DOWN:
#         rotation_y -= 1
#     elif symbol == key.LEFT:
#         rotation_x += 1
#     elif symbol == key.RIGHT:
#         rotation_x -= 1
def update(dt):
    global rotation_x
    global rotation_y
    global direction_x
    global direction_y
    rotation_x += direction_x*45*dt
    #rotation_y += direction_y*90*dt
    if abs(rotation_x) > 45:
        direction_x = -direction_x
    if abs(rotation_y) > 720.0:
        direction_y = -direction_y
        
    
    


pyglet.clock.schedule(update)
pyglet.app.run()