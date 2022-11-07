import pygame
from pygame.draw import *
from random import randint, uniform
import numpy as np

pygame.init()

FPS = 30
screen_size = (1000, 700)
screen = pygame.display.set_mode(screen_size)


RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]


def rotate(vec: list, angle: float):
    """
    :param vec: 2D vector
    :param angle: angle of rotation in radians
    :return: vector rotated on angle
    """
    rotation_matrix = np.array([[np.cos(angle), -np.sin(angle)],
                                [np.sin(angle), np.cos(angle)]])

    vec = np.matmul(vec, np.transpose(rotation_matrix))
    return vec


class Ball:
    """
    class of circles moving on screen
    """

    r_min = 80
    r_max = 80
    velocity_max = 10.0
    angle_velocity_max = 0.5
    lifetime = 80

    def __init__(self):
        self.pos = np.array(
            [uniform(Ball.r_max, screen_size[0] - Ball.r_max),
             uniform(Ball.r_max, screen_size[1] - Ball.r_max)])
        self.radius = uniform(Ball.r_min, Ball.r_max)
        self.color = COLORS[randint(0, 5)]
        self.velocity = np.array(
            [uniform(-Ball.velocity_max, Ball.velocity_max),
             uniform(-Ball.velocity_max, Ball.velocity_max)])  # for 1 tick
        self.angle_velocity = uniform(-Ball.angle_velocity_max, Ball.angle_velocity_max)
        self.lifetime = Ball.lifetime  # in ticks

    def tick(self):
        """
        Change circle position, velocity and radius for next frame
        :return: None
        """
        self.pos += self.velocity
        reflection = np.array([-1 if self.radius > self.pos[j] or screen_size[j] - self.radius < self.pos[j]
                               else 1 for j in range(2)])  # -1 if out of screen, else 1
        self.velocity = self.velocity * reflection

        self.angle_velocity = uniform(-Ball.angle_velocity_max, Ball.angle_velocity_max)  # angle velocity is random
        # for each frame
        self.velocity = rotate(self.velocity, self.angle_velocity)  # rotates vector of velocity due to angle velocity
        self.radius *= 1 - 1 / self.lifetime  # radius of circle decreases linear
        self.lifetime -= 1
        return None

    def print(self, surface: pygame.Surface):
        """
        Prints circle on screen
        :param surface: surface to draw on
        :return: None
        """
        circle(surface, self.color, self.pos, self.radius)
        return None

    def inside(self, pos):
        """
        Checks if dot on surface is inside the circle
        :param pos: position of dot
        :return: True if dot is inside
        """
        if sum((self.pos - np.array(pos)) ** 2) <= self.radius ** 2:
            return True
        else:
            return False


number_balls_popped = 0
number_balls = 0
current_balls = [Ball() for _ in range(3)]

pygame.font.init()
my_font = pygame.font.SysFont('Comic Sans MS', 20)


def generate_score(number_balls_popped, number_balls):
    """
    Generates score
    :return: score
    """
    if number_balls == 0:
        return 0
    else:
        return int(100 * number_balls_popped ** 2 / number_balls)


def generate_text_score(number_balls_popped, number_balls):
    """
    Renders text with number of popped balls, number of balls and score for surface
    :return: font
    """
    return my_font.render(' ' + str(number_balls_popped) + '/' + str(number_balls) + '  Score: ' +
                          str(generate_score(number_balls_popped, number_balls)), False, (255, 255, 255))


def add_score_to_file():
    """
    Changes scoreboard in file "Best scores.txt"
    """
    with open('Best scores.txt', 'r') as file:
        lines = file.readlines()

    score_list = [int(x.split()[1]) for x in lines[1:]]
    score_list.append(generate_score(number_balls_popped, number_balls))
    score_list.sort(reverse=True)
    if len(score_list) > 10:
        score_list = score_list[:10]

    with open('Best scores.txt', 'w') as file:
        file.write('Best scores:')
        for i in range(len(score_list)):
            file.write('\n' + str(i + 1) + '. ' + str(score_list[i]))

    return None


score = generate_text_score(number_balls_popped, number_balls)

clock = pygame.time.Clock()
finished = False
while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

        elif event.type == pygame.MOUSEBUTTONDOWN:
            for i in range(len(current_balls)):
                if current_balls[i].inside(event.pos):
                    number_balls_popped += 1
                    current_balls[i] = Ball()
                    score = generate_text_score(number_balls_popped, number_balls)
                    number_balls += 1

    for i in range(len(current_balls)):
        current_balls[i].tick()
        if current_balls[i].lifetime == 0:
            current_balls[i] = Ball()
            number_balls += 1
        score = generate_text_score(number_balls_popped, number_balls)
        current_balls[i].print(screen)

    screen.blit(score, (0, 0))
    pygame.display.update()
    screen.fill(BLACK)


add_score_to_file()

pygame.quit()
