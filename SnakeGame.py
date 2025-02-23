import turtle
import random
import time
from collections import deque
from abc import ABC, abstractmethod

class Subject(ABC):
    @abstractmethod
    def registerObserver(self, observer):
        pass
    @abstractmethod
    def _notifyObservers(self):
        pass

class Observer(ABC):
    @abstractmethod
    def update(self, data):
        pass

class Snake(Subject, Observer):
    _up = 2
    _down = 8
    _right = 6
    _left = 4
    _stop = 5
    _observers = []

    def __init__(self, border):
        self._borderSize = border.borderSize
        self._preyPosition = [0,0]
        self._initBody()
    def _initBody(self):
        self._dir = self._stop
        self._x = 0
        self._y = 0
        self._snake = deque([])
        self._isLonger = False
        self._time = 0.5
        self._snakeGrows()
    def registerObserver(self, observer):
        self._observers.append(observer)
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
        if self._x == self._preyPosition[0] and self._y == self._preyPosition[1]:
            self._notifyObservers()
        if self._dir == self._up:
            self._y = self._y + 20
        elif self._dir == self._down:
            self._y = self._y - 20
        elif self._dir == self._right:
            self._x = self._x + 20
        elif self._dir == self._left:
            self._x = self._x - 20
        self._move()
        if abs(self._snake[0].position()[0]) == self._borderSize//2 or abs(self._snake[0].position()[1]) == self._borderSize//2:
            time.sleep(2)
            for portion in self._snake:
                portion.reset()
            self._initBody()
            self._snakeGrows()
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
    def _notifyObservers(self):
        for observer in self._observers:
            observer.update(self._snake[0].position())
    def update(self, data):
        self._preyPosition = data
        self._isLonger = True
        if self._time > 0.025:
            self._time = self._time - 0.025
        else:
            self._time = 0.001



class Mouse(Observer, Subject):
    _hasObserver = False
    def __init__(self, predator, border):
        self._borderSize = border.borderSize
        self._mouse = turtle.Turtle()
        self._mouse.hideturtle()
        self._mouse.penup()
        self._mouse.color("white")
        self._mouse.left(90)
        self._mouse.speed(0)
        self._predator = predator
        self._changePosition()
    def _changePosition(self):
        self._x = ((int(random.random()*self._borderSize//20))-self._borderSize//40)*20
        self._y = ((int(random.random()*self._borderSize//20))-self._borderSize//40)*20
        self._mouse.hideturtle()
        self._mouse.setx(self._x)
        self._mouse.sety(self._y)
        self._mouse.showturtle()
        self._notifyObservers()
    def update(self, data):
        if data:
            self._changePosition()
    def registerObserver(self, observer):
        pass
    def _notifyObservers(self):
        self._predator.update(self._mouse.position())


class ScoreBoard(Observer):
    def __init__(self,screenSize):
        self._board = turtle.Turtle()
        self._board.hideturtle()
        self._board.penup()
        self._board.color("white")
        self._board.goto(0,-(screenSize//2 - 10))
        self._score = 0
        self._maxScore = 0
        self._board.write("Score: {}                Max Score: {}".format(self._score,self._maxScore), align="center")
    def update(self, data):
        self._score = self._score + 10
        if self._score > self._maxScore:
            self._maxScore = self._score
        self._board.clear()
        self._board.write("Score: {}                Max Score: {}".format(self._score,self._maxScore), align="center")

class Border():
    def __init__(self, screenSize):
        self._upper = screenSize//2 - 30
        self._bottom = -(screenSize//2 - 30)
        self._right = screenSize//2 - 30
        self._left = -(screenSize//2 - 30)
        self._border = turtle.Turtle()
        self._border.hideturtle()
        self._border.pensize(10)
        self._border.speed(0)
        self._border.penup()
        self._border.setx(self._left)
        self._border.sety(self._bottom)
        self._border.color("purple")
        self._border.pendown()
        self._border.setx(self._right)
        self._border.sety(self._upper)
        self._border.setx(self._left)
        self._border.sety(self._bottom)
    @property
    def borderSize(self):
        return self._upper - self._bottom

screenSize = 500
screen = turtle.Screen()
screen.screensize(screenSize,screenSize)
screen.bgcolor("black")
scoreBoard = ScoreBoard(screenSize)
border = Border(screenSize)
snake = Snake(border)
mouse = Mouse(snake, border)
snake.registerObserver(scoreBoard)
snake.registerObserver(mouse)
mouse.registerObserver(snake)

screen.listen()
screen.onkeypress(snake._goUp, "Up")
screen.onkeypress(snake._goDown, "Down")
screen.onkeypress(snake._goRight, "Right")
screen.onkeypress(snake._goLeft, "Left")

while 1:
    screen.update()
    snake.updatePos()

turtle.done()