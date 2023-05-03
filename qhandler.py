import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np
import random


class Experience:
    def __init__(self, ball, paddle, a, startScore):
        self.s = self.generateState(ball, paddle)
        self.a = a
        self.r = 0
        self.sPrime = []
        self.startScore = startScore

    def generateState(self, ball, paddle):
        return [paddle.x, ball.x, ball.y, ball.vx, ball.vy]
    
    def calcRew(self, newScore, ball, paddle):
        rew = 50 * (newScore - self.startScore)
        self.r = rew

    def setSPrime(self, dead, ball=0, paddle=0, ):
        if dead:
            self.sPrime = "terminal"
        else:
            self.sPrime = self.generateState(ball, paddle)

    def print(self):
        print("Paddle Loc: " + str(self.s[0]))
        print("Ball Loc: " + str(self.s[1])+ ", " + str(self.s[2]))
        print("Reward: " + str(self.r))
        print("Action: " + str(self.a))
        if not self.sPrime == "terminal":
            print("Paddle Loc new: " + str(self.sPrime[0]))
            print("Ball Loc new " + str(self.sPrime[1])+ ", " + str(self.sPrime[2]))
        else:
            print("new state is terminal")

class QHandler:
    def __init__(self):
        self.expReplay = []
        self.setupModel()
        self.epsilon = 1
        self.discount = 0.15
        self.deaths = 0
        self.highestScore = 0

    def setupModel(self):
        layer_1 = layers.Dense(units = 8, input_dim = 5, activation = "relu")
        layer_2 = layers.Dense(units = 8, activation = "relu")
        layer_3 = layers.Dense(units = 6, activation = "relu")
        layer_4 = layers.Dense(units = 3, activation = "linear")
        self.model = keras.Sequential([layer_1, layer_2, layer_4])

        self.model.compile(
            loss='mean_squared_error',
            optimizer="adam"
        )

        self.updateTargetNetwork()

    def updateTargetNetwork(self):
        self.targetModel = keras.models.clone_model(self.model)

    def getBestMove(self, ball, paddle):

        xs = np.array([[paddle.x, ball.x, ball.y, ball.vx, ball.vy]])
        predicts = self.model.predict(xs, verbose = 0)
        print(predicts)
        bestMove = np.argmax(predicts)
        if random.random() < self.epsilon:
            return random.randint(0,2)
        return bestMove

    def trainQNetwork(self, score):
        xs = []
        ys = []
        xsPrime = []
        if len(self.expReplay) < 500:
            return

        for ind, exp in enumerate(self.expReplay):
            xs.append(exp.s)
            if exp.sPrime == "terminal":
                xsPrime.append(exp.s)
            else:
                xsPrime.append(exp.sPrime)

        ys = self.model.predict(np.array(xs), verbose = 0)
        ysTarget = self.targetModel.predict(np.array(xsPrime), verbose = 0)
        for ind, exp in enumerate(self.expReplay):
            if exp.sPrime == "terminal":
                ys[ind][exp.a] = exp.r
            else:
                ys[ind][exp.a] = exp.r + self.discount * np.max(ysTarget[ind])

        


        # Cut down to 500 training examples


        print("Training on a sample of 1000 out of " + str(len(xs)) + " expierences")
        rng = np.random.default_rng()

        randIndices = range(len(xs))
        sampleIndices = rng.choice(np.array(randIndices), 1000)
        

        sampleXs = []
        sampleYs = []
        leftCount = 0
        rightCount = 0
        hitCount = 0
        deathCount = 0
        
        for i in sampleIndices:
            sampleXs.append(xs[i])
            sampleYs.append(ys[i])
            if self.expReplay[i].a == 1:
                rightCount += 1
            elif self.expReplay[i].a == 2:
                leftCount += 1
            if self.expReplay[i].r > 0:
                hitCount += 1
            if self.expReplay[i].r < 0:
                deathCount += 1
        print("Right Count: " + str(rightCount))
        print("Left Count: " + str(leftCount))
        print("Hit Count: " + str(hitCount))
        print("Death Count: " + str(deathCount))
        xsTensor = np.array(sampleXs)
        ysTensor = np.array(sampleYs)
        

        self.model.fit(xsTensor, ysTensor, epochs = 800, verbose = 0)
        self.deaths += 1
        if score > self.highestScore:
            self.highestScore = score
        
        print(self.deaths)
        print(self.highestScore)


        if self.highestScore > 5 and self.deaths > 400:
            self.epsilon = 0.5
        if self.highestScore > 10 and self.deaths > 800:
            self.epsilon = 0.35
        if self.highestScore > 15 and self.deaths > 1500:
            self.epsilon = 0.15
        if self.highestScore > 25 and self.deaths > 1700:
            self.epsilon = 0.05
        if self.highestScore > 100 and self.deaths > 2000:
            self.epsilon = 0.01


        if self.deaths % 15 == 0:
            self.updateTargetNetwork()
