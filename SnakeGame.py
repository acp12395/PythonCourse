import turtle
import random
import time
from collections import deque

class Snake():
    _up = 2
    _down = 8
    _right = 6
    _left = 4
    _stop = 5

    def __init__(self):
        self._dir = self._stop
        self._snake = deque([])
        self._x = 0
        self._y = 0
        self._isLonger = False
        self._time = 0.5
        self._snakeGrows()
        self._snakeGrows()
    def _goUp(self):
        if self._dir == self._right or self._dir == self._stop:
            self._dir = self._up
        elif self._dir == self._left:
            self._dir = self._up
    def _goDown(self):
        if self._dir == self._right or self._dir == self._stop:
            self._dir = self._down
        elif self._dir == self._left:
            self._dir = self._down
    def _goRight(self):
        if self._dir == self._up:
            self._dir = self._right
        elif self._dir == self._down:
            self._dir = self._right
        elif self._dir == self._stop:
            self._dir = self._right
    def _goLeft(self):
        if self._dir == self._up:
            self._dir = self._left
        elif self._dir == self._down:
            self._dir = self._left
        elif self._dir == self._stop:
            self._dir = self._left
    def updatePos(self):
        if self._dir == self._up:
            self._y = self._y + 10
        elif self._dir == self._down:
            self._y = self._y - 10
        elif self._dir == self._right:
            self._x = self._x + 10
        elif self._dir == self._left:
            self._x = self._x - 10
        self._move()
        time.sleep(self._time)
    def _snakeGrows(self):
        snake = turtle.Turtle()
        snake.hideturtle()
        snake.color("green")
        snake.penup()
        snake.shape("square")
        snake.speed(0)
        snake.goto(self._x,self._y)
        snake.showturtle()
        self._snake.appendleft(snake)
    def _move(self):
        if self._isLonger == True:
            self._snakeGrows()
            self._isLonger = False
        else:
            self._snake.rotate(1)
            self._snake[0].hideturtle()
            self._snake[0].setx(self._x)
            self._snake[0].sety(self._y)
            self._snake[0].showturtle()





class Mouse():
    def __init__(self):
        self._mouse = turtle.Turtle()
        self._mouse.hideturtle()
        self._mouse.penup()
        self._mouse.color("white")
        self._mouse.left(90)
        self._mouse.speed(0)
        self._changePosition()

    def _changePosition(self):
        self._x = (int(random.random()*48) - 24)*10
        self._y = (int(random.random()*48) - 24)*10
        self._mouse.hideturtle()
        self._mouse.setx(self._x)
        self._mouse.sety(self._y)
        self._mouse.showturtle()


s = turtle.Screen()
s.screensize(500,500,"black")
mouse = Mouse()
snake = Snake()

s.listen()
s.onkeypress(snake._goUp, "Up")
s.onkeypress(snake._goDown, "Down")
s.onkeypress(snake._goRight, "Right")
s.onkeypress(snake._goLeft, "Left")

while 1:
    s.update()
    snake.updatePos()

turtle.done()