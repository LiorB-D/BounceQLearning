import sys
import pygame
import ball
import paddle
import math

pygame.init()

size = 600
screen = pygame.display.set_mode((size, size))

myfont = pygame.font.SysFont("monospace", 25)
dt = 1


active = True

clock = pygame.time.Clock()
ball = ball.Ball(200, 200, 2, 3 * math.pi / 4, 10, size)
paddle = paddle.Paddle(0, 550, 250, 5, size, 2, ball)
ticks = 0

while active:
    ticks = (ticks + 1) % (1000 * dt)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            active = False
    

    screen.fill((0, 0, 0))
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        paddle.move(-1)
    if keys[pygame.K_RIGHT]:
        paddle.move(1)

    paddle.update(ticks, ball)

    pygame.draw.circle(screen, (50, 200, 50),
                       (ball.x, ball.y), ball.rad)  # DRAW CIRCLE
    pygame.draw.rect(screen, (200, 200, 200),
                     (paddle.x, paddle.y, paddle.w, paddle.h))
    ball.update(paddle)

    scoreboard = myfont.render("score: " + str(paddle.score), 50, (255,255,0))
    screen.blit(scoreboard, (250, 100))
    deathboard = myfont.render("deaths: " + str(paddle.qhandler.deaths), 50, (255,255,0))
    screen.blit(deathboard, (250, 130))
    highscoreboard = myfont.render("high score: " + str(paddle.qhandler.highestScore), 50, (255,255,0))
    screen.blit(highscoreboard, (250, 160))
    epsilonLbl = myfont.render("epsilon: " + str(paddle.qhandler.epsilon), 50, (255,255,0))
    screen.blit(epsilonLbl, (250, 190))
    pygame.display.update()
    
    clock.tick(100 * dt)
