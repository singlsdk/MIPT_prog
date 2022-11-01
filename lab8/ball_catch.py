import pygame
from pygame.draw import *
from random import randint
import numpy as np

pygame.init()

screen_size = (1000, 800)

FPS = 1
screen = pygame.display.set_mode(screen_size)

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]


def new_ball():
    """
    рисует новый шарик
    """
    r_min = 10
    r_max = 100
    x = randint(r_max, screen_size[0] - r_max)
    y = randint(r_max, screen_size[1] - r_max)
    r = randint(r_min, r_max)
    color = COLORS[randint(0, 5)]
    circle(screen, color, (x, y), r)
    return (x, y), r


pygame.display.update()
clock = pygame.time.Clock()
finished = False

pos_ball = (-1, 0)
r_ball = 0
number_balls_clicked = 0
number_balls = 0

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if sum((np.array(event.pos) - np.array(pos_ball)) ** 2) <= r_ball ** 2:  # Pythagoras
                number_balls_clicked += 1
                print('good click')
                break

    pos_ball, r_ball = new_ball()
    number_balls += 1
    pygame.display.update()
    screen.fill(BLACK)

print('You clicked on ', number_balls_clicked, '/', number_balls, 'balls')

pygame.quit()
