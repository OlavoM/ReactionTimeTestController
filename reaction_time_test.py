import pygame
import random
import time
from controls_util import get_joystick_connected

pygame.init()
pygame.display.set_caption("Reaction Time Test - Controller")

def  set_screen_config():
    global screen
    SCREEN_HEIGHT = 400
    SCREEN_WIDTH = 600
    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

def set_config():
    global font, fps_clock
    font = pygame.font.Font(None, 48)
    fps_clock = pygame.time.Clock()

    global WAITING, READY, RESULT
    WAITING = 0
    READY = 1
    RESULT = 2

    state = WAITING
    reaction_time = None
    start_time = None
    wait_delay = random.uniform(2, 5)
    square_color = red_color

    return state, reaction_time, start_time, wait_delay, square_color

def set_joystick():
    joystick_maybe = get_joystick_connected()
    if joystick_maybe is None:
        print("No controller detected")
        exit()
    else:
        return joystick_maybe

def set_colors():
    global red_color, blue_color, green_color, black_color
    red_color = pygame.Color(255, 0, 0)   
    blue_color = (0, 0, 255)
    green_color = (0, 255, 0)
    black_color = (0, 0, 0)

def draw_text(text, y):
    text_surface = font.render(text, True, (255, 255, 255))
    rect = text_surface.get_rect(center=(300, y))
    screen.blit(text_surface, rect)

def main(joystick_player_one, config):
    state, reaction_time, start_time, wait_delay, square_color = config

    running = True
    timer_started = False
    change_time = time.time() + wait_delay

    while running:
        screen.fill(black_color)

        # Center square
        pygame.draw.rect(screen, square_color, (200, 80, 200, 200))

        if state == WAITING:
            draw_text("Wait for green...", 300)
        elif state == READY:
            draw_text("PRESS NOW!", 300)
        elif state == RESULT:
            draw_text(f"Reaction time: {reaction_time * 1000:.0f} ms", 300)
            draw_text("Press any button to restart", 340)

        pygame.display.flip()
        fps_clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Detect any button from the joystick
            if event.type == pygame.JOYBUTTONDOWN:
                if state == READY:
                    reaction_time = time.time() - start_time
                    state = RESULT
                    square_color = blue_color
                elif state == RESULT:
                    # Restart
                    wait_delay = random.uniform(2, 5)
                    change_time = time.time() + wait_delay
                    state = WAITING
                    square_color = red_color
                elif state == WAITING:
                    # If you press before the green, it ignores.
                    pass

        # Change to green when its the right time
        if state == WAITING and time.time() >= change_time:
            square_color = green_color
            state = READY
            start_time = time.time()

    pygame.quit()



set_screen_config()
set_colors()
config_values = set_config()
joystick = set_joystick()
main(joystick, config_values)