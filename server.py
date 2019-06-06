from socket import *
from _thread import *
import random
import time
import json

import socketserver
import sys
from collections import deque

# constant
WIDTH = 1000
HEIGHT = 1000
REAL_WIDTH = WIDTH/20
REAL_HEIGHT = HEIGHT/20
DELAY = 0.1  # speed of the game
MAX_CLIENTS = 1

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


# def receive_message():
#     message = serverSocket.recv(1024).decode('utf-8')
#     # receive message from server, print it, close connection
#     print('From client', message)
#

#def broadcast(message, connection):
#    for client in clients:
#        if client[0] != connection:
#            try:
#                client[0].send(message).encode('utf-8')
#            except:
#                client[0].close()

                # if the link is broken, we remove the client
#                remove(clients)
# remove client if there isn't any more


# def remove(connection):
#     if connection in clients:
#         clients.remove(connection)



def switch_player(count):
    count = {
        1: "red",
        2: "blue",
        3: "green",
        4: "yellow",
        5: "orange",
    }
#def on_new_client(connection,addr):
#    global playercount
#    playercount = playercount +1
#    players.append(Player(switch_player(playercount), playercount-1))

#    while True:
 #       msg = connection.recv(1024).decode('utf-8')

 #       broadcast(msg, connection)





# accept up to two connections from clients, which
# must connect before we can move on
for i in range( 0, MAX_CLIENTS ):

    connectionSocket, addr = serverSocket.accept()

    clients.append((connectionSocket,addr))
    print (addr[0] +':'+str(addr[1]) + " connected" )

    connectionSocket.setblocking(0)
    #start_new_thread(on_new_client,(connectionSocket,addr))


# game
class Player:
    # player head
    def __init__(self, color, id):
        self.id = id
        self.length = 10
        self.direction = "up"
        self.color = color
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


player1 = Player("red", 0)
player2 = Player("blue", 1)
#player3 = Player("green",2)
playercount = 2
players = [player1, player2]  # ,player3]
food = Food()

print("server start")
message = json.dumps({"playercount": playercount})
print(message)
for i in range(0, MAX_CLIENTS):
    clients[i][0].send(message.encode('utf-8'))

# main loop
while True:
    for p in players:
        if p.x == food.x and p.y == food.y:
            p.eat()
            p.body.append(Body(p))
            food.move()
    for p in players:
        if p.length > len(p.body) and p.direction != "stop"and p.alive:
            p.body.append(Body(p))
        elif p.length == len(p.body)and p.alive:

            temp = p.body.popleft()
            del temp
            #p.body.append(Body(p))
            p.body.append(p)
        p.move()


    for p in players:
        for p2 in players:
            for seg in p2.body:
                if p.x == seg.x and p.y == seg.y:  # die
                    print("die",p.id,"seg:",seg.x)
                    playercount -= 1

                    p.direction = "stop"
                    p.alive = False
                    #while(len(p.body) != 0):
                     #   p.body.popleft()

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
                                   "y": food.y*20}})
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


