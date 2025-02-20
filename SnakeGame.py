import turtle
import random
import time
from collections import deque

class SNAKE():
    _up = 2
    _down = 8
    _right = 6
    _left = 4
    _stop = 5

    def __init__(self):
        self._snake = turtle.Turtle()
        self._snake.color("green")
        self._snake.pensize(5)
        self._dir = self._stop
        self._body = deque([list([0,0])])
        self._size = 10
    def _goUp(self):
        if self._dir == self._right or self._dir == self._stop:
            self._snake.left(90)
            self._dir = self._up
        elif self._dir == self._left:
            self._snake.right(90)
            self._dir = self._up
    def _goDown(self):
        if self._dir == self._right or self._dir == self._stop:
            self._snake.right(90)
            self._dir = self._down
        elif self._dir == self._left:
            self._snake.left(90)
            self._dir = self._down
    def _goRight(self):
        if self._dir == self._up:
            self._snake.right(90)
            self._dir = self._right
        elif self._dir == self._down:
            self._snake.left(90)
            self._dir = self._right
        elif self._dir == self._stop:
            self._dir = self._right
    def _goLeft(self):
        if self._dir == self._up:
            self._snake.left(90)
            self._dir = self._left
        elif self._dir == self._down:
            self._snake.right(90)
            self._dir = self._left
        elif self._dir == self._stop:
            self._snake.right(180)
            self._dir = self._left
    def updatePos(self):
        if self._dir != self._stop:
            self._snake.forward(20)
            self._body.append(self._snake.pos())
            self._snake.hideturtle()
            self._snake.color("black","black")
            if len(self._body) > self._size:
                self._snake.penup()
                self._snake.setx(self._body[0][0])
                self._snake.sety(self._body[0][1])
                self._snake.pendown()
                self._snake.setx(self._body[1][0])
                self._snake.sety(self._body[1][1])
                self._snake.penup()
                self._snake.setx(self._body[len(self._body) - 1][0])
                self._snake.sety(self._body[len(self._body) - 1][1])
                self._body.popleft()
                self._snake.pendown()
            self._snake.stamp()
            self._snake.color("green","green")
            self._snake.showturtle()



class MOUSE():
    def __init__(self):
        self._x = (int(random.random()*24) - 12)*20
        self._y = (int(random.random()*24) - 12)*20
        
        self._mouse = turtle.Turtle()
        self._mouse.hideturtle()
        self._mouse.penup()
        self._mouse.color("white")
        self._mouse.left(90)
        self._mouse.setx(self._x)
        self._mouse.sety(self._y)
        self._mouse.showturtle()


s = turtle.Screen()
s.screensize(500,500,"black")
mouse = MOUSE()
snake = SNAKE()

s.listen()
s.onkeypress(snake._goUp, "Up")
s.onkeypress(snake._goDown, "Down")
s.onkeypress(snake._goRight, "Right")
s.onkeypress(snake._goLeft, "Left")

while 1:
    s.update()
    snake.updatePos()
    time.sleep(.10)


turtle.done()