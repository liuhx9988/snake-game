# snake-game
this is a multi player snake game in python
only using turtle via tcp scoket

game description:
last player a live to win or have length of 100 to win
you can go out of screen and come back at other side to surprise your enemy
get the green circle to get longer

when someone win the game the game will pause 20s and exit
*can support mulit screen size and playercount
when change the server.py constant
defalut value
host: localhost
port: 43501
MAX_CLIENTS:2 #should support more then 2 clients but pocket lost might be too much
DELAY = 0.1
WIDTH = 1000
HEIGHT = 1000
MAX_LENGTH = 100 #length to win

pocket lost might cause the game to crash
