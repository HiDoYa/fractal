import math
import pygame
import random

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (205, 205, 205)

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
    #color = (color[0], color[1] - 10, color[2] - 10)
    color = (pos_1[0] / size[0] * 255, pos_1[1] / size[1] * 255, color[2] - 10)

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
    #color = (color[0], color[1] - 10, color[2] - 10)
    color = (0, color[1] - 10, 0)

    pos_2 = [pos_1[0] + math.cos(angle) * length, pos_1[1] + math.sin(angle) * length]
    pos_3 = [pos_2[0] + math.cos(angle / 2) * length, pos_2[1] + math.sin(angle / 2) * length]
    pos_4 = [pos_2[0] + math.cos(angle / 2 + math.pi / 2) * length, pos_2[1] + math.sin(angle / 2 + math.pi / 2) * length]

    pygame.draw.line(screen, color, pos_1, pos_2, 2)
    pygame.draw.line(screen, color, pos_2, pos_3, 2)
    pygame.draw.line(screen, color, pos_2, pos_4, 2)

    if n == 0:
        return

    tree(n - 1, pos_3, math.atan2(pos_3[1] - pos_2[1], pos_3[0] - pos_2[0]), length * 2 / 3, color)
    tree(n - 1, pos_4, math.atan2(pos_4[1] - pos_2[1], pos_4[0] - pos_2[0]), length * 2 / 3, color)

def mountain(n, pos_1, pos_2, color):
    color = (pos_1[0] / size[0] * 255, pos_1[1] / size[1] * 255, color[2])

    angle = math.atan2(pos_1[1] - pos_2[1], pos_2[0] - pos_1[0])
    angle_new = angle + math.pi / 4

    divisor = 2 + math.sqrt(2)
    magnitude = math.sqrt(math.pow((pos_2[1] - pos_1[1]), 2) + math.pow((pos_2[0] - pos_1[0]), 2))
    x = magnitude / divisor
    
    pos_a = [pos_1[0] + math.cos(angle) * x, pos_1[1] - math.sin(angle) * x]
    pos_b = [pos_a[0] + math.cos(angle_new) * x, pos_a[1] - math.sin(angle_new) * x]
    pos_c = [pos_2[0] - math.cos(angle) * x, pos_2[1] + math.sin(angle) * x]
    
    if n == 0:
        # Because don't want extra lines to be drawn
        pygame.draw.line(screen, color, pos_1, pos_a)
        pygame.draw.line(screen, color, pos_a, pos_b)
        pygame.draw.line(screen, color, pos_b, pos_c)
        pygame.draw.line(screen, color, pos_c, pos_2)
        return

    mountain(n - 1, pos_1, pos_a, color)
    mountain(n - 1, pos_a, pos_b, color)
    mountain(n - 1, pos_b, pos_c, color)
    mountain(n - 1, pos_c, pos_2, color)

def circle(n, pos, rad, color):
    color = (pos[0] / size[0] * 255, pos[1] / size[1] * 120, pos[0] / size[0] * 60)

    pygame.draw.circle(screen, color, pos, int(rad), 2)

    if n == 0:
        return

    pos_1 = [pos[0], int(pos[1] - rad / 2)]
    pos_2 = [pos[0], int(pos[1] + rad / 2)]
    pos_3 = [int(pos[0] - rad / 2), pos[1]]
    pos_4 = [int(pos[0] + rad / 2), pos[1]]

    pos_5 = [int(pos[0] + (rad / 2) * math.cos(math.pi/4)), int(pos[1] + (rad / 2) * math.sin(math.pi/4))]
    pos_6 = [int(pos[0] + (rad / 2) * math.cos(math.pi/4)), int(pos[1] - (rad / 2) * math.sin(math.pi/4))]
    pos_7 = [int(pos[0] - (rad / 2) * math.cos(math.pi/4)), int(pos[1] + (rad / 2) * math.sin(math.pi/4))]
    pos_8 = [int(pos[0] - (rad / 2) * math.cos(math.pi/4)), int(pos[1] - (rad / 2) * math.sin(math.pi/4))]

    circle(n - 1, pos_1, rad / 2, color)
    circle(n - 1, pos_2, rad / 2, color)
    circle(n - 1, pos_3, rad / 2, color)
    circle(n - 1, pos_4, rad / 2, color)

    circle(n - 1, pos_5, rad / 2, color)
    circle(n - 1, pos_6, rad / 2, color)
    circle(n - 1, pos_7, rad / 2, color)
    circle(n - 1, pos_8, rad / 2, color)

def circle_2(n, pos, rad, color):
    pygame.draw.circle(screen, color, pos, int(rad), 2)

n = 3

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    
    pressed = pygame.key.get_pressed()

    time_pass += 1
    if pressed[pygame.K_UP] and time_pass > 10:
        time_pass = 0
        n += 1
        print(n)
    if pressed[pygame.K_DOWN] and time_pass > 10:
        time_pass = 0
        n -= 1
        print(n)


    if pressed[pygame.K_1] and time_pass > 20:
        screen.fill(GRAY)
        triangle(10, [640, 120], [300, 600], [980, 600], WHITE)
        time_pass = 0
    if pressed[pygame.K_2] and time_pass > 20:
        screen.fill(GRAY)
        tree(15, [640, 0], math.pi / 2, 140, WHITE)
        time_pass = 0
    if pressed[pygame.K_3] and time_pass > 20:
        screen.fill(GRAY)
        mountain(6, [0, 500], [1280, 500], WHITE)
        time_pass = 0
    if pressed[pygame.K_4] and time_pass > 20:
        screen.fill(GRAY)
        circle(3, [640, 360], 300, WHITE)
        time_pass = 0


    pygame.display.flip()

    # 60 fps
    clock.tick(60)
