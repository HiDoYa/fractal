import math
import pygame
import random

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (105, 105, 105)

pygame.init()
size = (1280, 720)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Fractal")
clock = pygame.time.Clock()
time_pass = 0
done = False

screen.fill(GRAY)

def triangle(n, pos_1, pos_2, pos_3, color):
    # For cool flashing:
    #color = (color[0] - random.randint(10, 30), color[1] - random.randint(10, 30), color[2] - random.randint(10, 30))
    color = (color[0], color[1] - 20, color[2] - 20)
    pygame.draw.polygon(screen, color, [pos_1, pos_2, pos_3])

    point_a = [(pos_1[0] + pos_2[0]) / 2, (pos_2[1] + pos_1[1]) / 2]
    point_b = [(pos_3[0] + pos_1[0]) / 2, (pos_3[1] + pos_1[1]) / 2]
    point_c = [(pos_3[0] + pos_2[0]) / 2, pos_2[1]]

    if n == 0:
        return
    triangle(n - 1, pos_1, point_a, point_b, color)
    triangle(n - 1, point_a, pos_2, point_c, color)
    triangle(n - 1, point_b, point_c, pos_3, color)

def tree(n, pos_1, angle, length, color):
    color = (color[0], color[1] - 20, color[2] - 20)

    pos_2 = [pos_1[0] + math.cos(angle) * length, pos_1[1] + math.sin(angle) * length]
    pos_3 = [pos_2[0] + math.cos(angle / 2) * length, pos_2[1] + math.sin(angle / 2) * length]
    pos_4 = [pos_2[0] + math.cos(angle / 2 + math.pi / 2) * length, pos_2[1] + math.sin(angle / 2 + math.pi / 2) * length]

    pygame.draw.line(screen, color, pos_1, pos_2, 2)
    pygame.draw.line(screen, color, pos_2, pos_3, 2)
    pygame.draw.line(screen, color, pos_2, pos_4, 2)

    if n == 0:
        return

    tree(n - 1, pos_3, math.atan2(pos_3[1] - pos_2[1], pos_3[0] - pos_2[0]), length / 2, color)
    tree(n - 1, pos_4, math.atan2(pos_4[1] - pos_2[1], pos_4[0] - pos_2[0]), length / 2, color)

def mountain(n, pos_1, pos_2):
    angle = math.atan2(pos_2[0] - pos_1[0], pos_2[1] - pos_1[1])
    # TODO

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    
    pressed = pygame.key.get_pressed()

    time_pass += 1

    if pressed[pygame.K_1] and time_pass > 20:
        screen.fill(GRAY)
        triangle(6, [640, 120], [300, 600], [980, 600], WHITE)
        time_pass = 0
    if pressed[pygame.K_2] and time_pass > 20:
        screen.fill(GRAY)
        tree(10, [640, 0], math.pi / 2, 200, WHITE)
        time_pass = 0

    pygame.display.flip()

    # 60 fps
    clock.tick(60)
