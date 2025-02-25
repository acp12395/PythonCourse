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
        self._startListening()
    def _initBody(self):
        self._dir = self._stop
        self._changingDir = True
        self._x = 0
        self._y = 0
        self._snake = deque([])
        self._isLonger = False
        self._time = 0.5
        self._snakeGrows()
    def registerObserver(self, observer):
        self._observers.append(observer)
    def _goUp(self):
        if self._changingDir != True:
            if self._dir == self._right or self._dir == self._stop:
                self._dir = self._up
                self._changingDir = True
            elif self._dir == self._left:
                self._dir = self._up
                self._changingDir = True
    def _goDown(self):
        if self._changingDir != True:
            if self._dir == self._right or self._dir == self._stop:
                self._dir = self._down
                self._changingDir = True
            elif self._dir == self._left:
                self._dir = self._down
                self._changingDir = True
    def _goRight(self):
        if self._changingDir != True:
            if self._dir == self._up:
                self._dir = self._right
                self._changingDir = True
            elif self._dir == self._down:
                self._dir = self._right
                self._changingDir = True
            elif self._dir == self._stop:
                self._dir = self._right
                self._changingDir = True
    def _goLeft(self):
        if self._changingDir != True:
            if self._dir == self._up:
                self._dir = self._left
                self._changingDir = True
            elif self._dir == self._down:
                self._dir = self._left
                self._changingDir = True
            elif self._dir == self._stop:
                self._dir = self._left
                self._changingDir = True
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
        self._changingDir = False
        self._move()
        if abs(self._snake[0].position()[0]) == self._borderSize//2 or abs(self._snake[0].position()[1]) == self._borderSize//2:
            self._reset()
        for bodyPartIndex in range(1, len(self._snake)):
            if self._snake[0].position()[0] == self._snake[bodyPartIndex].position()[0] and self._snake[0].position()[1] == self._snake[bodyPartIndex].position()[1]:
                if self._dir != self._stop:
                    self._reset()
                    break
        time.sleep(self._time)
    def _reset(self):
        time.sleep(2)
        self._notifyObservers()
        for portion in self._snake:
            portion.reset()
        self._initBody()
        self._snakeGrows()
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
        data = list([self._snake[0].position()[0],self._snake[0].position()[1]])
        if self._x == self._preyPosition[0] and self._y == self._preyPosition[1]:
            data.append(True)
        else:
            data.append(False)
        for observer in self._observers:
            observer.update(data)
    def update(self, data):
        self._preyPosition = data
        for bodyPart in self._snake:
            if bodyPart.position() == self._preyPosition:
                return False
        self._isLonger = True
        if self._time > 0.025:
            self._time = self._time - 0.025
        else:
            self._time = 0.001
        return True
        

    def _startListening(self):
        turtle.onkeypress(self._goUp, "Up")
        turtle.onkeypress(self._goDown, "Down")
        turtle.onkeypress(self._goRight, "Right")
        turtle.onkeypress(self._goLeft, "Left")
        turtle.listen()


class Mouse(Observer, Subject):
    _hasObserver = False
    def __init__(self, predator, border):
        self._borderSize = border.borderSize - 20
        self._mouse = turtle.Turtle()
        self._mouse.hideturtle()
        self._mouse.penup()
        self._mouse.color("white")
        self._mouse.left(90)
        self._mouse.speed(0)
        self._predator = predator
        self._changePosition()
    def _changePosition(self):
        success = False
        while not success:
            self._x = ((int(random.random()*self._borderSize//20))-self._borderSize//40)*20
            self._y = ((int(random.random()*self._borderSize//20))-self._borderSize//40)*20
            success = self._notifyObservers()
        self._mouse.hideturtle()
        self._mouse.setx(self._x)
        self._mouse.sety(self._y)
        self._mouse.showturtle()
        
    def update(self, data):
        if data[0] == self._x and data[1] == self._y:
            self._changePosition()
    def registerObserver(self, observer):
        pass
    def _notifyObservers(self):
        position = (self._x,self._y)
        return self._predator.update(position)


class ScoreBoard(Observer):
    def __init__(self, border):
        self._borderSize = border.borderSize
        self._board = turtle.Turtle()
        self._board.hideturtle()
        self._board.penup()
        self._board.color("white")
        self._board.goto(0,-(self._borderSize//2 + 20))
        self._score = 0
        self._maxScore = 0
        self._board.write("Score: {}                Max Score: {}".format(self._score,self._maxScore), align="center")
    def update(self, data):
        if data[2]:
            self._score = self._score + 10
            if self._score > self._maxScore:
                self._maxScore = self._score
        else:
            self._score = 0
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
#canvas = screen.getcanvas()
root = screen.getcanvas().winfo_toplevel()

border = Border(screenSize)
scoreBoard = ScoreBoard(border)
snake = Snake(border)
mouse = Mouse(snake, border)
snake.registerObserver(scoreBoard)
snake.registerObserver(mouse)
mouse.registerObserver(snake)


def on_close():
    global running
    running = False

root.protocol("WM_DELETE_WINDOW", on_close)

running = True

while running:
    screen.update()
    snake.updatePos()