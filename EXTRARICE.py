'''
Author: Muhammad Ali Zia
Title: Brick Breaker
Date: 23-06-2016
'''

import time
import random
from tkinter import *

root = Tk()
root.title("Bounce v1.0")
root.geometry("500x500")
root.resizable(height=False, width=False)
root.wm_attributes("-topmost", 1)
canvas = Canvas(width=500, height=500, bd=0, highlightthickness=0)
canvas.pack()
startPaddleModTime = 0

playerReady = False

rectX = [
    [5, 100],
    [100, 200],
    [200, 300],
    [300, 400],
    [400, 495],
    [5, 100],
    [100, 200],
    [200, 300],
    [300, 400],
    [400, 495],
    [5, 100],
    [100, 200],
    [200, 300],
    [300, 400],
    [400, 495],
    [5, 100],
    [100, 200],
    [200, 300],
    [300, 400],
    [400, 495],
    [5, 100],
    [100, 200],
    [200, 300],
    [300, 400],
    [400, 495],
]

rectY = [
    [40, 60],
    [40, 60],
    [40, 60],
    [40, 60],
    [40, 60],
    [60, 80],
    [60, 80],
    [60, 80],
    [60, 80],
    [60, 80],
    [80, 100],
    [80, 100],
    [80, 100],
    [80, 100],
    [80, 100],
    [100, 120],
    [100, 120],
    [100, 120],
    [100, 120],
    [100, 120],
    [20, 40],
    [20, 40],
    [20, 40],
    [20, 40],
    [20, 40]
]


def drawBricks(x1, y1, x2, y2, i, color):
    canvas.create_rectangle(x1, y1, x2, y2, fill=color, width=2, tag=str(i))


for i in range(0, 25):
    j = 0
    if i == 2:
        color = "yellow"
    elif i == 19:
        color = "turquoise"
    elif i == 5:
        color = "lawn green"
    elif i == 11:
        color = "moccasin"
    else:
        color = "firebrick"
    drawBricks(rectX[i][j], rectY[i][j], rectX[i][j + 1], rectY[i][j + 1], i, color)


def startGame(event):
    print("Game Started")
    canvas.delete("pressed")
    while ball.groundHit != True:
        currentTime = time.time()
        ball.draw(rectX, rectY)
        paddle.draw()
        root.update_idletasks()
        root.update()
        time.sleep(0.01)

        if ((currentTime - ball.startBallSpeedModTime) >= 5 and (
                currentTime - ball.startBallSpeedModTime) <= 6) and ball.ballSpeedPower == True:
            print("ball speed mod over!!!")
            if ball.speed > 0:
                ball.speed = 5
            elif ball.speed < 0:
                ball.speed = -5
            ball.ballSpeedPower = False

            ball.currentPosition = ball.canvas.coords(ball.position)
            ball.canvas.delete("ballInitial")
            ball.position = canvas.create_oval(ball.currentPosition[0], ball.currentPosition[1],
                                               ball.currentPosition[2], ball.currentPosition[3], fill="red")
            ball.ballSpeedPower = False

        if ((currentTime - ball.startPaddleSpeedModTime) >= 5 and (
                currentTime - ball.startPaddleSpeedModTime) <= 6) and ball.paddleSpeedPower1 == True:
            paddle.paddleSpeed = 4
            paddleCoordinates = paddle.canvas.coords(paddle.position)
            canvas.delete("paddleInitial")
            paddle.position = paddle.canvas.create_rectangle(paddleCoordinates[0], paddleCoordinates[1],
                                                             paddleCoordinates[2], paddleCoordinates[3], fill="black",
                                                             tag="paddleInitial", width=2)
            ball.paddleSpeedPower1 = False

        if ((currentTime - ball.startPaddleModTime) >= 5 and (
                currentTime - ball.startPaddleModTime) <= 6) and ball.paddleSpeedPower == True:
            ball.restorePaddle("black")
            ball.paddleSpeedPower = False


class Ball:
    def __init__(self, canvas, paddle, color):
        self.canvas = canvas
        self.paddle = paddle
        self.position = canvas.create_oval(245, 460, 255, 470, fill=color, tag="ballInitial")
        angle = [-3, -2, -1, 1, 2, 3]
        random.shuffle(angle)
        self.direction = angle[0]
        self.speed = -5
        self.startPaddleModTime = 0
        self.startPaddleSpeedModTime = 0
        self.paddleSpeedPower = True
        self.paddleSpeedPower1 = True
        self.startBallSpeedModTime = 0
        self.ballSpeedPower = True
        self.lifeLineMod = False
        self.groundHit = False

    def restoreBall(event):
        currentPosition = self.canvas.coords(self.position)
        self.canvas.delete("ballInitial")
        self.position = canvas.create_oval(currentPosition[0], currentPosition[1], currentPosition[2],
                                           currentPosition[3], fill="red")

    def restorePaddle(self, color):
        paddleCoordinates = paddle.canvas.coords(paddle.position)
        canvas.delete("paddleInitial")
        paddleCoordinates[0] += 13
        paddleCoordinates[2] -= 13
        paddle.position = paddle.canvas.create_rectangle(paddleCoordinates[0], paddleCoordinates[1],
                                                         paddleCoordinates[2], paddleCoordinates[3], fill=color,
                                                         tag="paddleInitial")

    def draw(self, brickX, brickY):
        self.canvas.move(self.position, self.direction, self.speed)
        currentPosition = self.canvas.coords(self.position)
        paddlePosition = self.canvas.coords(self.paddle.position)
        if currentPosition[1] <= 0:
            self.speed *= -1
        if currentPosition[3] >= 500:
            print("GameOver")
            self.canvas.create_text(250, 250, text="The ball hit the ground you stupid human!", tag="pressed",
                                    font=("Times", 16))
            self.canvas.create_text(250, 285, text="Game Over", tag="pressed2", font=("Times", 20))

            ball.groundHit = True
        if currentPosition[0] <= 0:
            self.direction *= -1
        if currentPosition[2] >= 500:
            self.direction *= -1
        if self.lifeLineMod == True and currentPosition[3] >= 477:
            print("In Mod If")
            canvas.delete("LifeLineMod")
            self.speed *= -1
            self.lifeLineMod = False

        if currentPosition[2] >= paddlePosition[0] and currentPosition[0] <= paddlePosition[2] and currentPosition[3] >= \
                paddlePosition[1] and currentPosition[3] >= paddlePosition[3]:
            print("Collide")
            self.speed *= -1

        for i in range(0, 25):
            if currentPosition[2] >= brickX[i][0] and currentPosition[0] <= brickX[i][1] and currentPosition[1] >= \
                    brickY[i][0] and currentPosition[3] <= brickY[i][1]:  # and currentPosition[3]>=brickY[i][1]:
                self.speed *= -1
                canvas.delete(str(i + 1))
                '''
                print(brickX[i+1][0])
                print(brickX[i+1][1])
                print(brickY[i+1][0])
                print(brickY[i+1][1])
                '''
                brickX[i][0] = brickX[i][1] = brickY[i][0] = brickY[i][1] = 0

                if i == 19:
                    self.canvas.create_line(0, 476, 500, 476, width=2, fill="turquoise", tag="LifeLineMod")
                    self.lifeLineMod = True

                if i == 5:
                    print("Ball Speed Mod")
                    self.speed = 2
                    self.startBallSpeedModTime = time.time()

                if i == 11:
                    print("Paddle Speed Mod")
                    paddleCoordinates = paddle.canvas.coords(paddle.position)
                    canvas.delete("paddleInitial")
                    paddle.position = paddle.canvas.create_rectangle(paddleCoordinates[0], paddleCoordinates[1],
                                                                     paddleCoordinates[2], paddleCoordinates[3],
                                                                     fill="moccasin", tag="paddleInitial", width=2)
                    paddle.paddleSpeed = 8
                    self.startPaddleSpeedModTime = time.time()

                if i == 2:
                    paddleCoordinates = paddle.canvas.coords(paddle.position)
                    canvas.delete("paddleInitial")
                    paddleCoordinates[0] -= 13
                    paddleCoordinates[2] += 13
                    paddle.position = paddle.canvas.create_rectangle(paddleCoordinates[0], paddleCoordinates[1],
                                                                     paddleCoordinates[2], paddleCoordinates[3],
                                                                     fill="yellow", tag="paddleInitial", width=2)
                    self.startPaddleModTime = time.time()

                break


class Paddle:
    def __init__(self, canvas, color):
        self.canvas = canvas
        self.paddleSpeed = 4
        self.paddleSpeedL = self.paddleSpeed
        self.paddleSpeedR = self.paddleSpeed
        self.direction = 0
        self.x1 = 215
        self.x2 = 285
        self.y1 = 470
        self.y2 = 475
        self.position = self.canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2, fill=color,
                                                     tag="paddleInitial")

        self.canvas.bind_all('<KeyPress-Right>', self.moveRight)
        self.canvas.bind_all('<KeyRelease-Right>', self.moveStop)

        self.canvas.bind_all('<KeyPress-Left>', self.moveLeft)
        self.canvas.bind_all('<KeyRelease-Left>', self.moveStop)

    def moveLeft(self, event):
        currentPosition = self.canvas.coords(self.position)
        if currentPosition[0] >= 2:
            self.direction = self.paddleSpeedL
            self.direction *= -1
            self.paddleSpeedR = self.paddleSpeed

    def moveRight(self, event):
        currentPosition = self.canvas.coords(self.position)
        if currentPosition[2] <= 498:
            self.direction = self.paddleSpeedR
            self.direction *= 1
            self.paddleSpeedL = self.paddleSpeed

    def moveStop(self, event):
        self.direction = 0

    def changeSize(self):
        self.x1 = 200
        self.x2 = 320

    def draw(self):
        self.canvas.move(self.position, self.direction, 0)
        currentPosition = self.canvas.coords(self.position)
        if currentPosition[0] <= 0:
            self.paddleSpeedL = 0
        if currentPosition[2] >= 500:
            self.paddleSpeedR = 0


paddle = Paddle(canvas, "black")
ball = Ball(canvas, paddle, "red")

canvas.create_text(250, 250, text="Hit Spacebar when ready", tag="pressed", font=("Times", 12))
canvas.bind_all("<space>", startGame)

root.mainloop()