import math
import ball
import qhandler

class Paddle:
    def __init__(self, x, y, w, h, screenSize, v, ball):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.v = v
        self.respSpeed = 50
        self.screenSize = screenSize
        self.score = 0
        self.qhandler = qhandler.QHandler()
        self.currentExp = qhandler.Experience(ball, self, 0, 0)
        self.currDirection = 0 # 0 - Nothing, 1 - right, 2 - left

    def move(self, direction):
        self.x += direction * self.v
        if self.x < 0 or self.x + self.w > self.screenSize:
            self.x -= direction * self.v

    def update(self, ticks, ball):
        if ticks % self.respSpeed == 0:
            bestMove = self.qhandler.getBestMove(ball, self)

            self.currDirection = bestMove
            if self.currDirection == 2 and self.x < 10:
                self.currDirection == 0
            if self.currDirection == 1 and self.x + self.w > self.screenSize - 10:
                self.currDirection == 0
            
            self.currentExp = qhandler.Experience(ball, self, self.currDirection, self.score)
            
        if ticks % self.respSpeed == self.respSpeed - 1:
            self.currentExp.calcRew(self.score, ball, self)
            self.currentExp.setSPrime(False, ball, self)
            self.addExp()
        if self.qhandler.deaths > -1:
            if self.currDirection == 1:
                self.move(1)
            elif self.currDirection == 2:
                self.move(-1)

    def lossAndReset(self):
        self.currentExp.r = -100
        self.currentExp.setSPrime(True)
        self.addExp()
        self.qhandler.trainQNetwork(self.score)
        self.score = 0
        
    
    def addExp(self):
        self.qhandler.expReplay.append(self.currentExp)
        #self.currentExp.print()
        #self.qhandler.expReplay[0].print()
        