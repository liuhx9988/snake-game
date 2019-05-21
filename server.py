from socket import *
from _thread import *
import random
import sys
from collections import deque

# constant
WIDTH = 1000
HEIGHT = 1000
REAL_WIDTH = WIDTH/20
REAL_HEIGHT = HEIGHT/20
DELAY = 0.1  # speed of the game

# setup socket to wait for connections
serverPort = 43500
serverSocket = socket(AF_INET, SOCK_STREAM)  # TCP (reliable)
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) # make port reusable
serverSocket.bind(('', serverPort))
serverSocket.listen(1)


def receive_message():
    message = serverSocket.recv(1024).decode('utf-8')
    # receive message from server, print it, close connection
    print('From client', message)



def broadcast(message, connection):
    for client in clients:
        if client[0] != connection:
            try:
                client[0].send(message).encode('utf-8')
            except:
                client[0].close()

                # if the link is broken, we remove the client
                remove(clients)
#remove client if there isn't any more
def remove(connection):
    if connection in clients:
        clients.remove(connection)

def on_new_client(connection,addr):
    while True:
        msg = connection.recv(1024).decode('utf-8')
        broadcast(msg, connection)



clients = []

#accept up to two connections from clients, which
# must connect before we can move on
for i in range(0, MAX_CLIENTS):
    connectionSocket, addr = serverSocket.accept()
    clients.append((connectionSocket,addr))
    print (addr[0] +':'+str(addr[1]) + " connected" )
    start_new_thread(on_new_client,(connectionSocket,addr))


# game
class Player:
    # player head
    def __init__(self, color):
        self.length = 20
        self.direction = "stop"
        self.color(color)
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
        self.x
        self.y

    def update(self):
        self.x = self.body.x
        self.y = self.body.y


class Food:
    def __init__(self):
        self.x = 0
        self.y = 200  # start cor

    def move(self):
        self.x = random.randint(1-REAL_WIDTH/2, REAL_WIDTH/2-1)
        self.y = random.randint(1-REAL_HEIGHT/2, REAL_HEIGHT/2-1)

player1 = Player("red")
player2 = Player("blue")
# player3 = Player("green")
playercount = 2
players= [player1, player2]  # ,player3]
food = Food()



# main loop
while True:
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