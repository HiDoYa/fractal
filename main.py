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
done = False

def triangle(n, pos_1, pos_2, pos_3, color):
    # For cool flashing:
    #color = (color[0] - random.randint(10, 30), color[1] - random.randint(10, 30), color[2] - random.randint(10, 30))
    color = (color[0], color[1] - 10, color[2] - 10)
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

def juliana_hopkins(n, pos, multiplier):
    def func(x):
        return x * x * x
    
    color = WHITE
    pts = []

    for i in range(-10, 10):
        pts.append([int(pos[0] + i * 5), int(pos[1] + func(i / 10) * multiplier)])

    for i in range(0, len(pts)):
        if i != 0:
            pygame.draw.line(screen, color, pts[i - 1], pts[i], 2)

    if n == 0:
        return

    juliana_hopkins(n - 1, pts[len(pts) - 1], multiplier * 3 / 4)
    juliana_hopkins(n - 1, pts[0], multiplier * 3 / 4)

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    
    screen.fill(GRAY)

    # triangle(6, [640, 120], [300, 600], [980, 600], WHITE)
    # tree(10, [640, 0], math.pi / 2, 200, WHITE)
    juliana_hopkins(3, [640, 320], 90)
    juliana_hopkins(3, [640, 320], -90)
    pygame.display.flip()

    # 60 fps
    clock.tick(60)
