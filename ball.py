import math
import random

class Ball:
    def __init__(self, initX, initY, initV, initTheta, rad, screenSize):
        self.x = initX
        self.y = initY
        self.initTheta = initTheta
        self.initX = initX
        self.initY = initY
        self.vx = initV * math.cos(initTheta)
        self.vy = initV * math.sin(initTheta)
        self.rad = rad
        self.initV = initV
        self.screenSize = screenSize
        

    def update(self, paddle):
        self.x += self.vx
        self.y += self.vy

        self.bounce()
        if self.intersecting(paddle):
            paddle.score += 1
            self.y = paddle.y - self.rad
            newTheta = random.uniform(6 * math.pi / 5, 9 * math.pi / 5)
            self.vx = self.initV * math.cos(newTheta)
            self.vy = self.initV * math.sin(newTheta)

        # Check if lost
        if self.y + self.rad > self.screenSize:
            paddle.lossAndReset()
            self.reset()
        

    def bounce(self):
        if self.x + self.rad > self.screenSize:
            self.vx *= -1
        if self.x - self.rad < 0:
            self.vx *= -1
        if self.y - self.rad < 0:
            self.vy *= -1

    def intersecting(self, paddle):
        if self.x <= paddle.x + paddle.w and self.x >= paddle.x:
            if self.y + self.rad >= paddle.y and self.y - self.rad <= paddle.y + paddle.h:
                return True

        return False
    
    def reset(self):
        self.x = self.initX
        self.y = self.initY
        newTheta = random.uniform(6 * math.pi / 5, 9 * math.pi / 5)
        self.vx = self.initV * math.cos(newTheta)
        self.vy = self.initV * math.sin(newTheta)