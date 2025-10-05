from enum import Enum
import pygame
from pygame.locals import *

class Direction(Enum):
    UP = "up"
    DOWN = "down"
    RIGHT = "right"
    LEFT = "left"


def get_joystick_connected():
    # Xbox Controller
    pygame.joystick.init()
    joystick_count = pygame.joystick.get_count()
    if joystick_count == 0:
        return None
    else:
        joystick_connected = pygame.joystick.Joystick(0)
        joystick_connected.init()
        return joystick_connected


def get_dPad_direction(joystick_connected):
    d_pad = (joystick_connected.get_hat(0)[0], joystick_connected.get_hat(0)[1])
    if d_pad == (1, 0):
        return Direction.RIGHT
    elif d_pad == (-1, 0):
        return Direction.LEFT
    elif d_pad == (0, 1):
        return Direction.UP
    elif d_pad == (0, -1):
        return Direction.DOWN


def get_analog_stick_direction(joystick_connected):
    x_axis = joystick_connected.get_axis(0)
    y_axis = joystick_connected.get_axis(1)

    # Threshold for avoid direction detection mistakes (analogic dead zone)
    threshold = 0.3

    # Diagonal threshold
    dThreshold = 0.5

    if x_axis > threshold and y_axis < dThreshold and y_axis > -dThreshold:
        return Direction.RIGHT
    elif x_axis < -threshold and y_axis < dThreshold and y_axis > -dThreshold:
        return Direction.LEFT
    elif y_axis > threshold and x_axis < dThreshold and x_axis > -dThreshold:
        return Direction.DOWN
    elif y_axis < -threshold and x_axis < dThreshold and x_axis > -dThreshold:
        return Direction.UP


def get_key_direction(event):
    if event.key==K_RIGHT or event.key==ord("d"):
        return Direction.RIGHT
    if event.key==K_LEFT or event.key==ord("a"):
        return Direction.LEFT
    if event.key==K_UP or event.key==ord("w"):
        return Direction.UP
    if event.key==K_DOWN or event.key==ord("s"):
        return Direction.DOWN
    if event.key==K_ESCAPE:
        pygame.event.post(pygame.event.Event(QUIT))
