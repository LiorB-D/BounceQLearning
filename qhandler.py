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
        self.r =  50 * (newScore - self.startScore) - 0.005 * np.abs(paddle.x - ball.x)

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
        layer_2 = layers.Dense(units = 16, activation = "relu")
        layer_3 = layers.Dense(units = 16, activation = "relu")
        layer_4 = layers.Dense(units = 3, activation = "linear")
        self.model = keras.Sequential([layer_1, layer_2, layer_3, layer_4])

        self.model.compile(
            loss='mean_squared_error'
        )

        predicts = self.model.predict(np.array([[5, 5, 5, 1, 2]]))

    def getBestMove(self, ball, paddle):

        if random.random() < self.epsilon:
            return random.randint(0,2)

        xs = np.array([[paddle.x, ball.x, ball.y, ball.vx, ball.vy]])
        predicts = self.model.predict(xs)
        print(predicts)
        bestMove = np.argmax(predicts)

        return bestMove

    def trainQNetwork(self, score):
        xs = []
        ys = []
        for ind, exp in enumerate(self.expReplay):
            if (1 + ind) / len(self.expReplay) < random.random():
                xs.append(exp.s)
                y = self.model.predict(np.array([exp.s]))[0]
                if exp.sPrime == "terminal":
                    y[exp.a] = exp.r
                else:
                    y[exp.a] = exp.r + self.discount * np.max(self.model.predict(np.array([exp.sPrime])))
                
                ys.append(y)

        # Cut down to 100 training examples

            
        rng = np.random.default_rng()
        xsTensor = rng.choice(np.array(xs), 100)
        ysTensor = rng.choice(np.array(ys), 100)
        self.model.fit(xsTensor, ysTensor, epochs = 50, verbose = 1)
        self.deaths += 1
        if score > self.highestScore:
            self.highestScore = score
        
        print(self.deaths)
        print(self.highestScore)
        if self.deaths > 10:
            self.epsilon = 0.5
        if self.highestScore > 2 and self.deaths > 10:
            self.epsilon = 0.35
        if self.highestScore > 3 and self.deaths > 10:
            self.epsilon = 0.15
        if self.highestScore > 5 and self.deaths > 10:
            self.epsilon = 0.05
        if self.highestScore > 10 and self.deaths > 10:
            self.epsilon = 0.01
