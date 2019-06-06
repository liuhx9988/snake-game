from socket import *
import random
import time
import json
from collections import deque

# constant
WIDTH = 1000
HEIGHT = 1000
DELAY = 0.1  # speed of the game
MAX_CLIENTS = 2
MAX_LENGTH = 100 #length to win


REAL_WIDTH = WIDTH/20
REAL_HEIGHT = HEIGHT/20
# Global scope
playercount = 0
players = []
clients = []
# setup socket to wait for connections
serverPort = 43501
serverSocket = socket(AF_INET, SOCK_STREAM)  # TCP (reliable)
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) # make port reusable
serverSocket.bind(('', serverPort))
serverSocket.listen(1)



# accept up to two connections from clients, which
# must connect before we can move on
for i in range( 0, MAX_CLIENTS ):

    connectionSocket, addr = serverSocket.accept()

    clients.append((connectionSocket,addr))
    print (addr[0] +':'+str(addr[1]) + " connected" )

    connectionSocket.setblocking(0)



# game
class Player:
    # player head
    def __init__(self, id):
        self.id = id
        self.length = 10
        self.direction = "up"
        self.alive = True
        # self.head.goto(0,0)   # start cor
        self.x = random.randint(1-REAL_WIDTH/2, REAL_WIDTH/2-1)
        self.y = random.randint(1-REAL_HEIGHT/2, REAL_HEIGHT/2-1)
        self.body = deque()
    # player movement

    def move(self):
        if self.direction == "up":
            self.y = self.y + 1
            if self.y > REAL_HEIGHT/2-1:
                self.y = -self.y
        if self.direction == "down":
            self.y = self.y - 1
            if self.y < 1 - REAL_HEIGHT/2:
                self.y = - self.y
        if self.direction == "left":
            self.x = self.x - 1
            if self.x < 1 - REAL_WIDTH/2:
                self.x = - self.x
        if self.direction == "right":
            self.x = self.x + 1
            if self.x > REAL_WIDTH/2-1:
                self.x = -self.x

    def eat(self):
        self.length += 1

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


class Body:  # base segment of snake
    def __init__(self, p):
        self.body = p
        self.x = p.x
        self.y = p.y
        #p.move()
        # for p2 in players:
        #     if p2.x == self.x and p2.y == self.y:
        #         print("die?")
    def update(self):
        self.x = self.body.x
        self.y = self.body.y


class Food:
    def __init__(self):
        self.x = 0
        self.y = 20  # start cor

    def move(self):
        self.x = random.randint(1-REAL_WIDTH/2, REAL_WIDTH/2-1)
        self.y = random.randint(1-REAL_HEIGHT/2, REAL_HEIGHT/2-1)



food = Food()
for i in range(0, MAX_CLIENTS):
    players.append(Player(i))
    playercount += 1
print("server start")
message = json.dumps({"playercount": playercount})
print(message)
for i in range(0, MAX_CLIENTS):
    clients[i][0].send(message.encode('utf-8'))

winner = -1
Not_end = True
# main loop
while Not_end:
    for p in players:
        if p.x == food.x and p.y == food.y:
            p.eat()
            p.body.append(Body(p))
            if p.length > MAX_LENGTH:
                winner= p.id

            food.move()
    for p in players:
        if p.length > len(p.body) and p.direction != "stop"and p.alive:
            p.body.append(Body(p))
        elif p.length == len(p.body)and p.alive:

            temp = p.body.popleft()
            del temp
            #p.body.append(Body(p))
            p.body.append(Body(p))
        p.move()


    for p in players:
        for p2 in players:
            for seg in p2.body:
                if p.x == seg.x and p.y == seg.y:  # die
                    #print("die",p.id,"seg:",seg.x)
                    playercount -= 1

                    p.direction = "stop"
                    p.alive = False
                    while(len(p.body) != 0):
                       p.body.popleft()
        if playercount == 1:
            p.direction = "stop"
            Not_end = False
            for p in players:
                if p.alive:
                    winner = p.id
    #for p in players:
        #p.body.append(p)
# send update to client
    temp = []
    for p in players:
        temp.append({"id": p.id,
                              "alive": p.alive,
                              "x":p.x*20,
                              "y":p.y*20,
                              "length":p.length})
    message = json.dumps({"player": temp,
                          "food": {"x": food.x*20,
                                   "y": food.y*20},
                          "alive": playercount,
                          "win":winner})
    #print(message)
    for i in range(0, MAX_CLIENTS):
        clients[i][0].send(message.encode('utf-8'))
        try:
            message = clients[i][0].recv(1024).decode('utf-8')
            if players[i].alive and message:
                print(message)
                if message == "up":
                    players[i].up()
                elif message == "down":
                    players[i].down()
                elif message == "left":
                    players[i].left()
                elif message == "right":
                    players[i].right()
        except Exception:
            pass
    # text = turtle.write("playercount : " + str(playercount), move=False, align="left", font=("Arial", 8, "normal"), color = "white")

    time.sleep(DELAY)

time.sleep(20)