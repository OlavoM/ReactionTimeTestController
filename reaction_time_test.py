import pygame
import random
import time
from controls_util import get_joystick_connected

# Inicializa o pygame
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

set_screen_config()
set_config()
joystick = set_joystick()
set_colors()


state = WAITING
reaction_time = None
start_time = None
wait_delay = random.uniform(2, 5)
square_color = red_color

def draw_text(text, y):
    text_surface = font.render(text, True, (255, 255, 255))
    rect = text_surface.get_rect(center=(300, y))
    screen.blit(text_surface, rect)

running = True
timer_started = False
change_time = time.time() + wait_delay

while running:
    screen.fill(black_color)

    # Center square
    pygame.draw.rect(screen, square_color, (200, 80, 200, 200))

    if state == WAITING:
        draw_text("Espere o verde...", 300)
    elif state == READY:
        draw_text("APERTE AGORA!", 300)
    elif state == RESULT:
        draw_text(f"Tempo: {reaction_time:.3f}s", 300)
        draw_text("Aperte qualquer botão para reiniciar", 340)

    pygame.display.flip()
    fps_clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Detecta qualquer botão do controle
        if event.type == pygame.JOYBUTTONDOWN:
            if state == READY:
                reaction_time = time.time() - start_time
                state = RESULT
                square_color = blue_color  # Azul após resposta
            elif state == RESULT:
                # Reinicia
                wait_delay = random.uniform(2, 5)
                change_time = time.time() + wait_delay
                state = WAITING
                square_color = red_color
            elif state == WAITING:
                # Se apertar antes do verde, ignora
                pass

    # Troca para verde quando chegar o momento
    if state == WAITING and time.time() >= change_time:
        square_color = green_color
        state = READY
        start_time = time.time()

pygame.quit()
