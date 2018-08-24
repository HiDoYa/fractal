from cmath import sqrt
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
        pygame.draw.line(screen, color, pos_1, pos_a, 2)
        pygame.draw.line(screen, color, pos_a, pos_b, 2)
        pygame.draw.line(screen, color, pos_b, pos_c, 2)
        pygame.draw.line(screen, color, pos_c, pos_2, 2)
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

def apollonian_wrp(n, p_1, rad, parts, color):
    r_1 = rad
    r_2 = rad / parts
    r_3 = rad * (parts - 1) / parts

    p_2 = [int(p_1[0] - r_3), p_1[1]]
    p_3 = [int(p_1[0] + r_2), p_1[1]]

    pygame.draw.circle(screen, color, p_1, int(r_1), 1)
    pygame.draw.circle(screen, color, p_2, int(r_2), 1)
    pygame.draw.circle(screen, color, p_3, int(r_3), 1)

    apollonian_rec(n, p_1, p_2, p_3, -1 / r_1, 1 / r_2, 1 / r_3, color)

def apollonian_rec(n, p_1, p_2, p_3, b_1, b_2, b_3, color):
    # Descartes theorem
    num_to_root = b_1 * b_2 + b_1 * b_3 + b_2 * b_3
    if num_to_root < 0:
        return
    r = 2 * math.sqrt(b_1 * b_2 + b_1 * b_3 + b_2 * b_3)
    s = b_1 + b_2 + b_3

    b_4_1 = s + r
    b_4_2 = s - r

    # Get position
    z_1 = p_1[0] + p_1[1] * 1j
    z_2 = p_2[0] + p_2[1] * 1j
    z_3 = p_3[0] + p_3[1] * 1j

    #r = 2 * sqrt(b_1 * z_1 + b_2 * z_2 + z_3)
    r = 2 * sqrt(b_1 * z_1 * b_2 * z_2 + b_1 * z_1 * b_3 * z_3 + b_2 * z_2 * b_3 * z_3)
    s = b_1 * z_1 + b_2 * z_2 + b_3 * z_3

    z_4_1 = [(r.real + s.real) / b_4_1, (r.imag + s.imag) / b_4_1]
    z_4_2 = [(-r.real + s.real) / b_4_2, (-r.imag + s.imag) / b_4_2]

    if b_4_1 > 0:
        try:
            pygame.draw.circle(screen, color, [int(z_4_1[0]), int(z_4_1[1])], int(abs(1 / b_4_1)), 1)
        except ValueError:
            pygame.draw.circle(screen, color, [int(z_4_1[0]), int(z_4_1[1])], int(abs(1 / b_4_1)), 0)
    if b_4_2 > 0:
        try:
            pygame.draw.circle(screen, color, [int(z_4_2[0]), int(z_4_2[1])], int(abs(1 / b_4_2)), 1)
        except ValueError:
            pygame.draw.circle(screen, color, [int(z_4_1[0]), int(z_4_1[1])], int(abs(1 / b_4_1)), 0)

    if n == 0:
        return

    apollonian_rec(n - 1, p_1, p_2, z_4_1, b_1, b_2, b_4_1, color)
    apollonian_rec(n - 1, p_1, p_2, z_4_2, b_1, b_2, b_4_2, color)

    apollonian_rec(n - 1, p_2, p_3, z_4_1, b_2, b_3, b_4_1, color)
    apollonian_rec(n - 1, p_2, p_3, z_4_2, b_2, b_3, b_4_2, color)

    apollonian_rec(n - 1, p_1, p_3, z_4_1, b_1, b_3, b_4_1, color)
    apollonian_rec(n - 1, p_1, p_3, z_4_2, b_1, b_3, b_4_2, color)

# z^3 is also interesting
def julia_z_update(n, z):
    c = 0
    if n == 0:
        c = -1.037 + 0.17j
    if n == 1:
        c = -0.52 + 0.57j
    if n == 2:
        c = -0.624 + 0.435j
    if n == 3:
        c = 0.26 + 0.54j
    if n == 4:
        c = -0.72 - 0.3275j
    return pow(z, 2) + c

def juliana_hopkins(n, color):
    for y in range(-360, 360):
        for x in range(-640, 640):
            a = x / 320
            b = y / 180
            julia(n, [a, b], color)

def julia(n, pos, color):
    color_factor = 4
    no_draw = False
    no_draw_pos = math.floor(255 / color_factor)
    z = pos[0] + pos[1] * 1j

    for x in range(0, math.floor(255 / color_factor)):
        z = julia_z_update(n, z)
        if math.sqrt(z.real * z.real + z.imag * z.imag) >= 2:
            # not in set
            no_draw = True
            no_draw_pos = x
            break;

    if no_draw_pos > 50:
        color = [0, 0, 0]
    else:
        color = [color[0], color[1] - no_draw_pos * color_factor, color[2]]
    pygame.draw.circle(screen, color, [int(pos[0] * 320 + 640), int(pos[1] * 180 + 360)], 1)

def mandelbrot_set(color):
    for y in range(-360, 360):
        for x in range(-640, 640):
            a = x / 320
            b = y / 180
            mand([a, b], color)

def mand_z_update(z, pos):
    c = pos[0] + pos[1] * 1j
    return pow(z, 2) + c

def mand(pos, color):
    color_factor = 3
    no_draw = False
    no_draw_pos = math.floor(255 / color_factor)
    z = 0

    for x in range(0, math.floor(255 / color_factor)):
        z = mand_z_update(z, pos)
        if math.sqrt(z.real * z.real + z.imag * z.imag) >= 2:
            # not in set
            no_draw = True
            no_draw_pos = x
            break;

    if no_draw_pos > 50:
        color = [0, 0, 0]
    else:
        color = [color[0], color[1] - no_draw_pos * color_factor, color[2] - no_draw_pos * color_factor]
    pygame.draw.circle(screen, color, [int(pos[0] * 320 + 640), int(pos[1] * 180 + 360)], 1)


text = pygame.font.SysFont("Gill Sans", 25)
tx_wait = text.render("Please wait a second for fractals to load.", False, BLACK)
tx_1 = text.render("Press 1-8 to see different fractals.", False, BLACK)
tx_2 = text.render("Press q, w, e, r, t to see different Julia set fractals.", False, BLACK)

# For testing purposes only
#n = 2

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    
    pressed = pygame.key.get_pressed()

    time_pass += 1

    # For testing purposes only
    #if pressed[pygame.K_UP] and time_pass > 10:
    #    time_pass = 0
    #    n += 1
    #    print(n)
    #if pressed[pygame.K_DOWN] and time_pass > 10:
    #    time_pass = 0
    #    n -= 1
    #    print(n)


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
        circle(3, [640, 360], 350, WHITE)
        time_pass = 0
    if pressed[pygame.K_5] and time_pass > 20:
        screen.fill(GRAY)
        apollonian_wrp(6, [640, 360], 350, 2, BLACK)
        time_pass = 0
    if pressed[pygame.K_6] and time_pass > 20:
        screen.fill(GRAY)
        apollonian_wrp(6, [640, 360], 350, 3, BLACK)
        time_pass = 0
    if pressed[pygame.K_7] and time_pass > 20:
        screen.fill(GRAY)
        apollonian_wrp(6, [640, 360], 350, 4, BLACK)
        time_pass = 0
    if pressed[pygame.K_8] and time_pass > 20:
        screen.fill(GRAY)
        mandelbrot_set(WHITE)
        time_pass = 0

    if pressed[pygame.K_q] and time_pass > 20:
        screen.fill(GRAY)
        juliana_hopkins(0, WHITE)
        time_pass = 0
    if pressed[pygame.K_w] and time_pass > 20:
        screen.fill(GRAY)
        juliana_hopkins(1, WHITE)
        time_pass = 0
    if pressed[pygame.K_e] and time_pass > 20:
        screen.fill(GRAY)
        juliana_hopkins(2, WHITE)
        time_pass = 0
    if pressed[pygame.K_r] and time_pass > 20:
        screen.fill(GRAY)
        juliana_hopkins(3, WHITE)
        time_pass = 0
    if pressed[pygame.K_t] and time_pass > 20:
        screen.fill(GRAY)
        juliana_hopkins(4, GRAY)
        time_pass = 0

    screen.blit(tx_1, (20, 40))
    screen.blit(tx_2, (20, 10))
    screen.blit(tx_wait, (850, 10))

    pygame.display.flip()

    # 60 fps
    clock.tick(60)
