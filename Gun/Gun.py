import math
from random import choice, uniform, randint
import numpy as np

import pygame

FPS = 30

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 800
HEIGHT = 600


class Gun:
    initial_f2_power = 20

    def __init__(self, screen):
        self.pos = [20, 550]
        self.screen = screen
        self.f2_power = Gun.initial_f2_power
        self.f2_on = 0
        self.an = 1
        self.color = GREY
        self.shots = 0

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        new_ball = Ball(self.screen, self.pos[0], self.pos[1])
        new_ball.r += 5
        self.an = math.atan2((event.pos[1] - new_ball.y), (event.pos[0] - new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = - self.f2_power * math.sin(self.an)
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = Gun.initial_f2_power
        self.shots += 1

    def move(self, direction):
        move_speed = 4
        if direction == 1 and gun.pos[0] < 800 - 20:
            self.pos[0] += move_speed
        elif direction == -1 and gun.pos[0] > 20:
            self.pos[0] -= move_speed

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.an = math.atan2((event.pos[1] - gun.pos[1]), (event.pos[0] - gun.pos[0]))
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self):
        pygame.draw.line(self.screen, self.color, self.pos,
                         np.array(self.pos) + self.f2_power * np.array([np.cos(self.an), np.sin(self.an)]),
                         width=5)
        return

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 70:
                self.f2_power += 1
            self.color = RED
        else:
            self.color = GREY


class Ball:
    def __init__(self, screen: pygame.Surface, x, y):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = BLACK
        self.live = 30

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        self.x += self.vx
        self.y -= self.vy
        acceleration = 3

        if self.r >= self.x or self.x >= self.screen.get_width() - self.r:
            self.vx = -self.vx

        k = 1.5  # k - attenuation coefficient
        floor = 550 - self.r
        if self.y >= floor:
            self.y += self.vy
            self.vx = self.vx / k
            self.vy = - self.vy / k
            print(self.vy)
            if self.vy < 2 * acceleration:
                print(777777)
                return True
            else:
                return False
        self.vy -= acceleration

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )

    def hittest(self, target):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            target: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        if (target.x - self.x) ** 2 + (target.y - self.y) ** 2 <= (target.r + self.r) ** 2:
            return True
        else:
            return False


class Target:
    points = 0

    def __init__(self, screen):
        self.screen = screen
        self.x = uniform(600, 780)
        self.y = uniform(300, 550)
        self.r = uniform(10, 50)
        self.color = RED
        self.live = 1
        self.vx = 0
        self.vy = 0

    def move(self):
        self.x += self.vx
        self.y += self.vy

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )


class TargetStanding(Target):
    points = 1

    def __init__(self, screen):
        super().__init__(screen)
        self.screen = screen
        self.r = uniform(10, 50)
        self.x = uniform(250, 740)
        self.y = uniform(100, 500 - self.r)
        self.color = RED
        self.live = 1
        self.vx = 0
        self.vy = 0


class TargetMoving(Target):
    points = 2

    def __init__(self, screen):
        super().__init__(screen)
        self.screen = screen
        self.r = uniform(10, 50)
        self.x = uniform(250, 740)
        self.y = uniform(100, 500 - self.r)
        self.color = BLUE
        self.live = 1
        self.half_period = randint(15, 30)
        self.step = 0
        self.x_end = uniform(250, 740)
        self.y_end = uniform(100, 500 - self.r)
        self.vx = (self.x_end - self.x) / self.half_period
        self.vy = (self.y_end - self.y) / self.half_period

    def move(self):
        self.x += self.vx
        self.y += self.vy
        if (self.step + 1) % self.half_period == 0:
            self.vx = -self.vx
            self.vy = -self.vy
            self.step = 0
        self.step += 1


class Bomb:

    def __init__(self, screen, gun):
        self.screen = screen
        self.x = gun.pos[0]
        self.y = 0
        self.r = 20
        self.color = GREEN
        self.live = 1
        self.vx = 0
        self.vy = 20

    def move(self):
        self.x += self.vx
        self.y += self.vy

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )

    def explosion_test(self, gun):
        if (gun.pos[0] - self.x) ** 2 + (gun.pos[1] - self.y) ** 2 <= self.r ** 2:
            return True
        else:
            return False


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet = 0
balls = []
bombs = []
pygame.font.init()
my_font = pygame.font.SysFont('Comic Sans MS', 20)

clock = pygame.time.Clock()
gun = Gun(screen)
TARGET_CLASSES = (TargetStanding, TargetMoving)
targets = [choice(TARGET_CLASSES)(screen) for _ in range(3)]
score = my_font.render(str(Target.points), False, (0, 0, 0))
screen.blit(score, (100, 100))
default_text_duration = 60
text_duration = 0
points = 0
shots = 0
direction = 0
right_key_down = 0
left_key_down = 0
finished = False
explosion = False

while not finished:
    screen.fill(WHITE)
    gun.move(direction)
    gun.draw()
    for target in targets:
        target.move()
        target.draw()
    for b in balls:
        b.draw()
    if randint(1, 50) == 1:
        bombs.append(Bomb(screen, gun))

    for bomb in bombs:
        bomb.draw()
        if bomb.explosion_test(gun):
            explosion = True
            finished = True

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

        elif event.type == pygame.KEYDOWN:
            if event.key == 1073741903:
                right_key_down = True
                direction = 1
            elif event.key == 1073741904:
                left_key_down = True
                direction = -1
        elif event.type == pygame.KEYUP:
            direction = 0
            if event.key == 1073741903:
                right_key_down = 0
            if event.key == 1073741904:
                left_key_down = 0

        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire2_start(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire2_end(event)
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)

    if direction == 0:
        if right_key_down:
            direction = 1
        elif left_key_down:
            direction = -1

    for bomb in bombs:
        bomb.move()

    for ball in balls:
        delete_ball = ball.move()
        if delete_ball:
            balls.remove(ball)
        else:
            for i in range(len(targets)):
                if ball.hittest(targets[i]) and targets[i].live:
                    points += type(targets[i]).points
                    targets[i].live = 0
                    targets[i] = choice(TARGET_CLASSES)(screen)
                    shots = gun.shots
                    gun.shots = 0
                    score = my_font.render(str(points), False, (0, 0, 0))
                    text_duration = default_text_duration

    '''
    is_balls_popped = [0 for _ in balls]
    for j in range(len(balls)):
        delete_ball = balls[j].move()
        if delete_ball:
            balls[j] = 0
        else:
            for i in range(len(targets)):
                if balls[j].hittest(targets[i]) and targets[i].live:
                    points += type(targets[i]).points
                    targets[i].live = 0
                    targets[i] = choice(TARGET_CLASSES)(screen)
                    shots = gun.shots
                    gun.shots = 0
                    score = my_font.render(str(points), False, (0, 0, 0))
                    text_duration = default_text_duration
    balls = list(filter(lambda x: False if x == 0 else True, balls))
    '''


    '''
    if text_duration > 0:
        gun.f2_on = 0
        screen.blit(my_font.render('Вы уничтожили цель за ' + str(shots) + ' выстрелов',
                                   False, (0, 0, 0)), (300, 560))
    if text_duration == 0:
        target = choice(TARGET_CLASSES)(screen)

    text_duration -= 1
    '''

    gun.power_up()
    screen.blit(score, (10, 10))
    pygame.display.update()

if explosion:
    screen.fill(WHITE)
    screen.blit(my_font.render('Game over', False, (0, 0, 0)), (300, 300))
    pygame.display.update()
    finished = False
    while not finished:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True

pygame.quit()
