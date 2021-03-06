import turtle
import time
import random
from socket import *
import sys

# import queue
from collections import deque


serverName = '72.233.138.35'
serverPort = 43500
clientSocket = socket(AF_INET, SOCK_STREAM)  # TCP socket
clientSocket.connect((serverName, serverPort))
# constant

WIDTH = 1000
HEIGHT = 1000
DELAY = 0.1  # speed of the game


# main screen
game = turtle.Screen()
game.tracer(0)
game.bgcolor("black")
game.title("Sanke Game")
game.setup(width=WIDTH, height=HEIGHT)


def send_data(dir):
    data = str(dir)
    clientSocket.send(data.encode('utf-8'))


class Player:
    # player head
    def __init__(self, color):
        self.head = turtle.Turtle()
        self.direction = "stop"
        self.length = 20
        self.head.speed(0)
        self.head.shape("square")
        self.head.color(color)
        self.head.penup()
        self.alive = True
        # self.head.goto(0,0)   # start cor
        x = random.randint(1-WIDTH/2, WIDTH/2-1)
        x = x - x % 20
        y = random.randint(1-HEIGHT/2, HEIGHT/2-1)
        y = y - y % 20
        self.head.goto(x, y)
        self.body = deque()
    # player movement

    def move(self):
        if self.direction == "up":
            self.head.sety(self.head.ycor() + 20)
            if self.head.ycor()>499:
                self.head.sety(-self.head.ycor())
        if self.direction == "down":
            self.head.sety(self.head.ycor() - 20)
            if self.head.ycor() < -499:
                self.head.sety(-self.head.ycor())
        if self.direction == "left":
            self.head.setx(self.head.xcor() - 20)
            if self.head.xcor() < -499:
                self.head.setx(-self.head.xcor())
        if self.direction == "right":
            self.head.setx(self.head.xcor() + 20)
            if self.head.xcor() > 499:
                self.head.setx(-self.head.xcor())

    def eat(self):
        self.length +=1

    # player movement control not allow go back
    def up(self):
        if self.direction != "down":
            self.direction = "up"

    def down(self):
        if self.direction != "up":
            self.direction = "down"

    def left(self):
        if self.direction != "right":
            self.direction = "left"

    def right(self):
        if self.direction != "left":
            self.direction = "right"


class Body: # base segment of snake
    def __init__(self, p):
        self.body = p
        self.seg = turtle.Turtle()
        self.seg.speed(0)
        self.seg.shape("square")
        self.seg.color("white")
        self.seg.penup()
        self.seg.goto(p.head.xcor(), p.head.ycor())

    def update(self):
        self.seg.goto(self.body.head.xcor(), self.body.head.ycor())


class Food:
    def __init__(self):
        self.food = turtle.Turtle()
        self.direction = "stop"
        self.food.speed(0)
        self.food.shape("circle")
        self.food.color("green")
        self.food.penup()
        self.food.goto(0, 200)   # start cor

    def move(self):
        x = random.randint(-499, 499)
        x= x- x%20
        y = random.randint(-499, 499)
        y = y - y % 20
        self.food.goto(x, y)


player1 = Player("red")
player2 = Player("blue")
# player3 = Player("green")
playercount = 2
players= [player1, player2]  # ,player3]
food = Food()

game.listen()
game.onkey(player1.up, "w")
game.onkey(player1.down, "s")
game.onkey(player1.left, "a")
game.onkey(player1.right, "d")

game.onkey(player2.up, "Up")
game.onkey(player2.down, "Down")
game.onkey(player2.left, "Left")
game.onkey(player2.right, "Right")
while True:
    game.update()

    for p in players:
        if p.head.xcor() == food.food.xcor()and p.head.ycor() == food.food.ycor():
            p.eat()
            p.body.append(Body(p))
            food.move()
    for p in players:
        if p.length> len(p.body) and p.direction != "stop"and p.alive:
            p.body.append(Body(p))
        elif p.length == len(p.body)and p.alive:

            temp = p.body.popleft().seg.reset()
            del temp
            p.body.append(Body(p))

            # temp = p.body.popleft().seg.goto(p.body.head.xcor(), p.body.head.ycor())
            # p.body.append(temp)
            # cannot move body?

        p.move()

    for p in players:
        for p2 in players:
            for seg in p2.body:
                if p.head.xcor() == seg.seg.xcor()and p.head.ycor() == seg.seg.ycor():  # die

                    playercount -= 1

                    p.direction = "stop"
                    p.alive = False
                    p.head.reset()
                    while(len(p.body) != 0):
                        temp = p.body.popleft().seg.reset()
                        del temp

    # text = turtle.write("playercount : " + str(playercount), move=False, align="left", font=("Arial", 8, "normal"), color = "white")

    time.sleep(DELAY)


game.mainloop()