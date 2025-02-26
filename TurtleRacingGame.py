import turtle
import random

class PLAYER():
    def __init__(self, playerNo):
        self._t = turtle.Turtle(shape="turtle", visible=False)
        if playerNo == 1:
            self._t.color("green", "green")
            self._y = 140
            self._player = 1
        elif playerNo == 2:
            self._t.color("blue", "blue")
            self._y = -140
            self._player = 2
        self._t.penup()
        self._t.hideturtle()
        self._t.speed(10)
        self._drawGoal()
        self._x = self._goToInitialPos()
        self._t.shapesize(2,2,2)
        self._count = 0
        self._die = (1,2,3,4,5,6)
    def _drawGoal(self):
        self._t.pensize(5)
        self._t.sety(self._y - 30)
        self._t.setx(220)
        self._t.pendown()
        self._t.circle(30)
        self._t.penup()
        self._t.sety(self._y)
        self._t.pensize(2)
    def _goToInitialPos(self):
        x = -220
        self._t.setx(x)
        self._t.showturtle()
        self._t.pendown()
        return x
    def turn(self):
        self._count = self._count + 1
        turn = input("Press Enter for player {} turn...".format(self._player))
        turn = random.choice(self._die) * 10
        if self._t.pos()[0] + turn > 220:
            turn = 220 - self._t.pos()[0]
        self._t.forward(turn)
    @property
    def pos(self):
        return self._t.pos()[0]
    def reset(self):
        count = self._count
        self._count = 0
        for i in range(count):
            self._t.undo()


s = turtle.Screen()
s.title("Turtle racing")
s.bgcolor("gray")

players = (PLAYER(1), PLAYER(2))
play = True

while play:
    turn = True
    players[0].reset()
    players[1].reset()
    while players[0].pos < 220 and players[1].pos < 220:
        turn = turn ^ 1
        players[turn].turn()
    print("Player {} won!".format(int(turn) + 1))
    play = bool(int(input("Do you want to play again?\n 1) Yes\n 0) No\n")))
print("Please close window to finish...")

turtle.done()

