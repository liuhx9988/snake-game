import turtle
import time
import random
from socket import *
import json
import sys

# import queue
from collections import deque



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



class Player:
    # player head
    def __init__(self, color):
        self.head = turtle.Turtle()
        self.direction = "stop"
        self.length = 50
        self.head.speed(0)
        self.head.shape("square")
        self.head.color(color)
        self.color = color
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
        self.seg.color(p.color)
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

def switch_player(count):
    switcher  = {
        1: "red",
        2: "blue",
        3: "purple",
        4: "yellow",
        5: "orange"
    }
    return switcher.get(count, (random.random(),random.random(),random.random()))


def up():
    clientSocket.send("up".encode('utf-8'))
    print("sent UP")

def down():
    clientSocket.send("down".encode('utf-8'))


def left():
    clientSocket.send("left".encode('utf-8'))


def right():
    clientSocket.send("right".encode('utf-8'))


food = Food()

game.listen()
game.onkey(up, "w")
game.onkey(down, "s")
game.onkey(left, "a")
game.onkey(right, "d")

serverName = 'localhost'
serverPort = 43501
clientSocket = socket(AF_INET, SOCK_STREAM)  # TCP socket
clientSocket.connect((serverName, serverPort))

message = clientSocket.recv(1024).decode('utf-8')
data = json.loads(message)
players = []

for x in range(data["playercount"]):
    players.append(Player(switch_player(x+1)))

while True:
    game.update()
    message = clientSocket.recv(1024).decode('utf-8')
    print("Received: {}" .format(message))
    data = json.loads(message)
    #print(data["player"][0])
    # text = turtle.write("playercount : " + str(playercount), move=False, align="left", font=("Arial", 8, "normal"), color = "white")
    food.food.goto(data["food"]["x"],data["food"]["y"])
    for player in data["player"]:
        if player["alive"]:
            players[player["id"]].head.goto(player["x"],player["y"])

            if player["length"] > len(players[player["id"]].body):
                players[player["id"]].body.append(Body(players[player["id"]]))
            else:
                temp = players[player["id"]].body.popleft().seg.reset()
                del temp
                players[player["id"]].body.append(Body( players[player["id"]]))

#switch_player(x+1)
        else:
            players[player["id"]].head.reset()
            while (len(players[player["id"]].body) != 0):
                temp = players[player["id"]].body.popleft().seg.reset()
                del temp
    if data["win"] != -1:
        print("WIN")
        win_text = turtle.Turtle()
        win_text.color("deep pink")
        text = "Player "+switch_player(data["win"]+1)+" WIN!"
        #text = "player"
        win_text.write(text, move=False, align="left", font=("Arial", 50, "normal"))
        win_text.shape("square")
        win_text.speed(0)
        win_text.penup()
        win_text.goto(-800,0)
        win_text.hideturtle()
    #players

    #time.sleep(DELAY)

    for p in players:
        if p.length> len(p.body) and p.direction != "stop"and p.alive:
            p.body.append(Body(p))
        elif p.length == len(p.body)and p.alive:

            temp = p.body.popleft().seg.reset()
            del temp
            p.body.append(Body(p))
game.mainloop()


time.sleep(20)