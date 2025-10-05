import pygame
import random
import time
from controls_util import get_joystick_connected

# Inicializa o pygame
pygame.init()
pygame.display.set_caption("Reaction Time Test - Controller")

screen = pygame.display.set_mode((600, 400))

font = pygame.font.Font(None, 48)
clock = pygame.time.Clock()

# Conecta o controle
joystick = get_joystick_connected()
if joystick is None:
    print("Nenhum controle detectado!")
    exit()

# Estados do jogo
WAITING = 0
READY = 1
RESULT = 2

state = WAITING
reaction_time = None
start_time = None
wait_delay = random.uniform(2, 5)
color = (255, 0, 0)  # Vermelho

def draw_text(text, y):
    text_surface = font.render(text, True, (255, 255, 255))
    rect = text_surface.get_rect(center=(300, y))
    screen.blit(text_surface, rect)

running = True
timer_started = False
change_time = time.time() + wait_delay

while running:
    screen.fill((0, 0, 0))

    # Quadrado central
    pygame.draw.rect(screen, color, (250, 150, 100, 100))

    if state == WAITING:
        draw_text("Espere o verde...", 300)
    elif state == READY:
        draw_text("APERTE AGORA!", 300)
    elif state == RESULT:
        draw_text(f"Tempo: {reaction_time:.3f}s", 300)
        draw_text("Aperte qualquer botão para reiniciar", 340)

    pygame.display.flip()
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Detecta qualquer botão do controle
        if event.type == pygame.JOYBUTTONDOWN:
            if state == READY:
                reaction_time = time.time() - start_time
                state = RESULT
                color = (0, 0, 255)  # Azul após resposta
            elif state == RESULT:
                # Reinicia
                wait_delay = random.uniform(2, 5)
                change_time = time.time() + wait_delay
                state = WAITING
                color = (255, 0, 0)
            elif state == WAITING:
                # Se apertar antes do verde, ignora
                pass

    # Troca para verde quando chegar o momento
    if state == WAITING and time.time() >= change_time:
        color = (0, 255, 0)
        state = READY
        start_time = time.time()

pygame.quit()
