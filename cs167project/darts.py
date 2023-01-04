"""
Author: Fabian Gabriel
Date: 12/09/2022
Assignment: Final Project - CS-167
Citations and Acknowledgments:
    This code uses an external module graphics.py
    The Arrow class was build from a code provided by Prof. Davis (projectile.py)
    The button.py was provided by Prof. Davis (button.py)
    I did my reaserch on official parameters of the dart game using the following link:
        https://www.darting.com/Darts-Rules/General/
    Thank you to Prof. Davis and Prof. Kumar who gave me 
    a piece of advice on debugging the first versions of the code
    
"""

from math import sin, cos, pi
from button import Button
import graphics


class Arrow:
    def __init__(self, velocity, angle, height=1.73):
        """
        Parameters:
            velocity : a positive int
            angle : a positive float (in radians)
            height : 1.73 meters

        Return value: None

        """
        self.vel = graphics.Point(velocity * cos(angle), velocity * sin(angle))
        self.height = height
        self.position = graphics.Point(0, self.height)
        self.gravity = graphics.Point(0, -9.8)

    def __str__(self):
        return "Projectile at position " + str(self.position)

    def getPositon(self):
        return self.position

    def getAltitude(self):
        return self.position.y

    def getDistance(self):
        return self.position.x

    def update(self, dt):
        """
        Parameters:
            dt: a positive integer
                represents the change of time for the projectile

        Return value: None

        """
        if self.getDistance() < 2.43:
            self.vel = graphics.Point(
                self.vel.getX(), self.vel.getY() + (self.gravity.getY() * dt)
            )
            self.position = graphics.Point(
                self.position.getX() + self.vel.getX() * dt,
                self.position.getY() + self.vel.getY() * dt,
            )
        return


class arrowSymbol:
    def __init__(self, center):
        """
        Parameters:
            center: a graphics module Point object

        Return value: None

        """
        self.center = center
        self.cross1 = graphics.Line(
            graphics.Point(center.getX() - 10, center.getY() - 10),
            graphics.Point(center.getX() + 10, center.getY() + 10),
        )
        # the first part of the cross
        self.cross1.setWidth(4)
        self.cross1.setFill("red")
        self.cross2 = graphics.Line(
            graphics.Point(center.getX() + 10, center.getY() - 10),
            graphics.Point(center.getX() - 10, center.getY() + 10),
        )
        # the second part of the cross
        self.cross2.setWidth(4)
        self.cross2.setFill("red")

    def draw(self, win):
        """
        Parameters:
            win: a graphics module GraphWin object

        Return value: None

        """
        self.cross1.draw(win)
        self.cross2.draw(win)

    def undraw(self):
        self.cross1.undraw()
        self.cross2.undraw()


class Target:
    def __init__(self, center, radius):
        """
        Parameters:
            center: a graphics module Point object
            radius: a positive int

        Return value: None

        """
        colors = [
            graphics.color_rgb(255, 195, 197),
            "white",
            graphics.color_rgb(171, 215, 255),
        ] * 2
        values = ["100", "50", "20", "10", "5"]
        self.target = []
        self.values = []
        for count in range(5):
            circle = graphics.Circle(center, (radius * (1 - 0.2 * count)))
            circle.setFill(colors[count])
            circle.setWidth(3)
            self.target.append(circle)
            value = graphics.Text(
                graphics.Point(
                    center.getX() + (radius * 0.2 * count) + radius * 0.1, center.getY()
                ),
                values[count],
            )
            self.values.append(value)

    def draw(self, win):
        """
        Parameters:
            win: a graphics module GraphWin object

        Return value: None

        """
        # draws each circle of the target
        for circle in self.target:
            circle.draw(win)
        # draws the values of each circle
        for value in self.values:
            value.draw(win)


class selector:
    def __init__(self, position, win, upBttn, downBttn, strengthBttns, fire):
        """
        Parameters:
            position: a graphics module Point object
            win: a graphics module GraphWin object
            upBttn: a button module Button object
            downBttn: a button module Button object
            strengthBttns: a list of button module Button objects
            fire: a button module Button object

        Return value: None

        """
        # sets intial variables
        self.angle = 0
        self.win = win
        self.position = position
        self.arrowLength = 80
        self.back = graphics.Point(position.getX(), position.getY())
        self.front = graphics.Point(position.getX() - self.arrowLength, position.getY())
        # draws the intial arrow
        self.arrow = graphics.Line(self.front, self.back)
        self.arrow.setWidth(2)
        self.arrow.draw(self.win)
        # horizontal boundary for angle
        self.boundary1 = graphics.Line(
            self.back,
            graphics.Point(self.back.getX(), position.getY() - self.arrowLength),
        )
        # vertical boundary for angle
        self.boundary2 = graphics.Line(
            self.back,
            graphics.Point(position.getX() - self.arrowLength, self.back.getY()),
        )
        self.boundary1.setFill("grey")
        self.boundary2.setFill("grey")
        self.boundary1.draw(self.win)
        self.boundary2.draw(self.win)
        self.upBttn = upBttn
        self.downBttn = downBttn
        self.buttons = strengthBttns
        self.fire = fire
        # the projectile function cannot work with a zero value
        # we need to assign a very low velocity to simulate its motion
        self.value = 0.01

    def update(self):
        """
        Parameters:
            self: the object itseld

        Return value: a tuple (value, angle)
                        value, a postive int (speed)
                        angle, a positive float (angle in rad)

        """
        click = graphics.Point(0, 0)
        while True:
            click = self.win.getMouse()
            # moves the arrow up
            if self.upBttn.contains(click) == True and self.angle <= (pi / 2):
                self.angle = self.angle + pi / 180
                self.arrow.undraw()
                self.front = graphics.Point(
                    self.back.getX() - self.arrowLength * cos(self.angle),
                    self.back.getY() - self.arrowLength * sin(self.angle),
                )
                self.arrow = graphics.Line(self.front, self.back)
                self.arrow.setWidth(2)
                self.arrow.draw(self.win)
            # moves the arrow down
            elif self.downBttn.contains(click) == True and self.angle > 0:
                self.angle = self.angle - pi / 180
                self.arrow.undraw()
                self.front = graphics.Point(
                    self.back.getX() - self.arrowLength * cos(self.angle),
                    # the number 1.395767 represents the cosine difference of one radian 
                    self.front.getY() + 1.395767,
                )
                self.arrow = graphics.Line(self.front, self.back)
                self.arrow.setWidth(2)
                self.arrow.draw(self.win)

            # sets the selected speed
            for strenghtBttn in self.buttons:
                if strenghtBttn.contains(click) == True:
                    strenghtBttn.setFill("red")
                    self.value = self.buttons.index(strenghtBttn) + 1
                else:
                    strenghtBttn.setFill(graphics.color_rgb(255, 195, 197))
            if self.fire.contains(click) == True:
                return (self.value, self.angle)

    def reset(self):
        # undraws the arrow for next trial
        self.arrow.undraw()
        self.back = graphics.Point(self.position.getX(), self.position.getY())
        self.front = graphics.Point(
            self.position.getX() - self.arrowLength, self.position.getY()
        )
        self.arrow = graphics.Line(self.front, self.back)
        self.arrow.setWidth(2)
        self.arrow.draw(self.win)
        self.angle = 0
        self.value = 0.01


class scoreBoard:
    def __init__(self, win):
        """
        Parameters:
            win: a graphics module GraphWin object

        Return value: None

        """
        self.win = win
        self.total = 0
        self.totalScore = graphics.Text(
            graphics.Point(
                (self.win.width // 2 - self.win.height // 3) // 2,
                self.win.height // 2 - self.win.height // 3,
            ),
            "Total score:",
        )
        self.totalScore.setStyle("bold")
        self.totalScore.setSize(15)
        self.totalValue = graphics.Text(
            graphics.Point(
                (self.win.width // 2 - self.win.height // 3) // 2,
                self.win.height // 2 - self.win.height // 3 + 20,
            ),
            "0",
        )
        self.latest = 0
        self.latestScore = graphics.Text(
            graphics.Point(
                (self.win.width // 2 + self.win.height // 3)
                + (self.win.width // 2 - self.win.height // 3) // 2,
                self.win.height // 2 - self.win.height // 3,
            ),
            "Latest score:",
        )
        self.latestScore.setStyle("bold")
        self.latestScore.setSize(15)
        self.latestValue = graphics.Text(
            graphics.Point(
                (self.win.width // 2 + self.win.height // 3)
                + (self.win.width // 2 - self.win.height // 3) // 2,
                self.win.height // 2 - self.win.height // 3 + 20,
            ),
            "0",
        )
        self.arrowsLeft = graphics.Text(
            graphics.Point(
                self.win.width // 2, (self.win.height // 2) + self.win.height // 3 + 85
            ),
            "Arrows left: 5",
        )

    def draw(self, win):
        self.totalScore.draw(win)
        self.latestScore.draw(win)
        self.totalValue.draw(win)
        self.latestValue.draw(win)
        self.arrowsLeft.draw(win)

    def undraw(self):
        self.totalScore.undraw()
        self.latestScore.undraw()
        self.totalValue.undraw()
        self.latestValue.undraw()
        self.arrowsLeft.undraw()

    def update(self, cross):
        """
        This method compares the location of the cross on the target and determines the score achived

        Parameters:
            cross: a main module arrowSymbol object

        Return value: None

        """
        self.cross = cross
        self.win.radius = self.win.height // 3
        ycoord = self.cross.center.getY()
        if (
            ycoord > self.win.height // 2 - self.win.radius
            and ycoord < self.win.height // 2 - self.win.radius + self.win.radius * 0.2
        ) or (
            ycoord > self.win.height // 2 + self.win.radius * 0.8
            and ycoord < self.win.height // 2 + self.win.radius
        ):
            self.latest = 5
        elif (
            ycoord > self.win.height // 2 - self.win.radius + self.win.radius * 0.2
            and ycoord < self.win.height // 2 - self.win.radius + self.win.radius * 0.4
        ) or (
            ycoord > self.win.height // 2 + self.win.radius * 0.6
            and ycoord < self.win.height // 2 + self.win.radius * 0.8
        ):
            self.latest = 10
        elif (
            ycoord > self.win.height // 2 - self.win.radius + self.win.radius * 0.4
            and ycoord < self.win.height // 2 - self.win.radius + self.win.radius * 0.6
        ) or (
            ycoord > self.win.height // 2 + self.win.radius * 0.4
            and ycoord < self.win.height // 2 + self.win.radius * 0.6
        ):
            self.latest = 20
        elif (
            ycoord > self.win.height // 2 - self.win.radius + self.win.radius * 0.6
            and ycoord < self.win.height // 2 - self.win.radius + self.win.radius * 0.8
        ) or (
            ycoord > self.win.height // 2 + self.win.radius * 0.2
            and ycoord < self.win.height // 2 + self.win.radius * 0.4
        ):
            self.latest = 50
        elif (
            ycoord > self.win.height // 2 - self.win.radius + self.win.radius * 0.8
            and ycoord < self.win.height // 2 + self.win.radius * 0.2
        ):
            self.latest = 100
        else:
            self.latest = 0
        if self.latest > 0:
            self.latestValue.setText(str(self.latest))
        else:
            self.latestValue.setText("Missed")
        self.total = self.total + self.latest
        self.totalValue.setText(str(self.total))


class gameInterface:
    def __init__(self, width, height):
        """
        Parameters:
            width: a positive int
            height: a positive int

        Return value: None

        """
        self.win = graphics.GraphWin("Darts", width, height)
        self.width = width
        self.height = height
        radius = height // 3
        self.radius = radius

    def drawTitles(self, win):
        # game title
        title = graphics.Text(graphics.Point(self.width // 2, 50), "Darts!")
        title.setSize(30)
        title.setStyle("bold")
        title.draw(self.win)
        # angle title
        self.angleTitle = graphics.Text(
            graphics.Point(
                self.width // 2 + self.radius + 75,
                (self.height // 2) + self.radius - 20,
            ),
            "Angle",
        )
        self.angleTitle.setSize(15)
        self.angleTitle.draw(self.win)
        # speed title
        self.strengthTitle = graphics.Text(
            graphics.Point(
                self.width // 2 - (200 + 4 * 20),
                ((self.height // 2) + self.radius + 20),
            ),
            "Speed (m/s)",
        )
        self.strengthTitle.setSize(15)
        self.strengthTitle.draw(self.win)

    def drawTarget(self, win):
        target = Target(graphics.Point(self.width // 2, self.height // 2), self.radius)
        target.draw(self.win)

    def drawButtons(self, win):
        # FIRE button
        self.fireButton = Button(
            graphics.Point(
                self.width // 2 - 60, ((self.height // 2) + self.radius + 30)
            ),
            graphics.Point(
                self.width // 2 + 60, ((self.height // 2) + self.radius + 70)
            ),
        )
        self.fireButton.setText("FIRE")
        self.fireButton.setTextSize(20)
        self.fireButton.setTextColor("red")
        self.fireButton.setOutline("red")
        self.fireButton.setWidth(5)
        self.fireButton.draw(self.win)

        # UP angle button
        self.upBttn = Button(
            graphics.Point(
                (self.width // 2 + self.radius) + 0,
                ((self.height // 2) + self.radius + 30),
            ),
            graphics.Point(
                (self.width // 2 + self.radius) + 45,
                ((self.height // 2) + self.radius + 50),
            ),
        )
        self.upBttn.setWidth(3)
        self.upBttn.setText("Up")
        self.upBttn.draw(self.win)

        # DOWN angle button
        self.downBttn = Button(
            graphics.Point(
                (self.width // 2 + self.radius) + 0,
                ((self.height // 2) + self.radius + 50),
            ),
            graphics.Point(
                (self.width // 2 + self.radius) + 45,
                ((self.height // 2) + self.radius + 70),
            ),
        )
        self.downBttn.setWidth(3)
        self.downBttn.setText("Down")
        self.downBttn.draw(self.win)

        # SPEED buttons
        self.buttons = []
        for strenght in range(8, 0, -1):
            strenghtBttn = Button(
                graphics.Point(
                    self.width // 2 - (200 + strenght * 20),
                    ((self.height // 2) + self.radius + 40),
                ),
                graphics.Point(
                    self.width // 2 - (180 + strenght * 20),
                    ((self.height // 2) + self.radius + 60),
                ),
            )
            strenghtBttn.setFill(graphics.color_rgb(255, 195, 197))
            strenghtBttn.setWidth(3)
            strenghtBttn.setText(str(9 - strenght))
            self.buttons.append(strenghtBttn)

        for strenghtBttn in self.buttons:
            strenghtBttn.draw(self.win)

    def draw(self, win):
        """
        Parameters:
            win: a graphics module GraphWin object

        Return value: None

        """
        self.drawTitles(self.win)
        self.drawTarget(self.win)
        self.drawButtons(self.win)

    def setSelector(self):
        self.selector = selector(
            graphics.Point(
                (self.width // 2 + self.radius) + 150,
                ((self.height // 2) + self.radius + 70),
            ),
            self.win,
            self.upBttn,
            self.downBttn,
            self.buttons,
            self.fireButton,
        )

    def selection(self):

        return self.selector.update()

    def reset(self):
        self.selector.reset()


class gameOver:
    def __init__(self, win, scoreBoard):
        """
        Draws a pop up message after all five arrows have been fired

        Parameters:
            win: a graphics module GraphWin object
            scoreBoard: a main module scoreBoard object

        Return value: None

        """
        self.win = win
        self.scoreBoard = scoreBoard
        # pop up rectangle
        self.popUp = graphics.Rectangle(
            graphics.Point(250, 200), graphics.Point(550, 400)
        )
        self.popUp.setFill("gold")
        # game over title
        self.gameOverText = graphics.Text(
            graphics.Point(self.win.width // 2, self.win.height // 2 - 75), "Game Over!"
        )
        self.gameOverText.setStyle("bold")
        self.gameOverText.setSize(20)
        # total score title
        self.totalScore = graphics.Text(
            graphics.Point(self.win.width // 2, self.win.height // 2 - 55),
            "Your total score is:",
        )
        # total score value title
        self.totalScoreValue = graphics.Text(
            graphics.Point(self.win.width // 2, self.win.height // 2 + -35),
            str(self.scoreBoard.total),
        )
        # instrutions to close the window
        self.instructions = graphics.Text(
            graphics.Point(self.win.width // 2, self.win.height // 2),
            "Press anywhere to close the window",
        )
        # replay button
        self.replayButton = Button(graphics.Point(325, 325), graphics.Point(475, 375))
        self.replayButton.setText("PLAY AGAIN")
        self.replayButton.setTextSize(20)
        self.replayButton.setFill("black")
        self.replayButton.setTextColor("white")

    def draw(self):
        self.popUp.draw(self.win)
        self.gameOverText.draw(self.win)
        self.totalScore.draw(self.win)
        self.instructions.draw(self.win)
        self.replayButton.draw(self.win)
        self.totalScoreValue.draw(self.win)

    def undraw(self):
        self.popUp.undraw()
        self.gameOverText.undraw()
        self.totalScore.undraw()
        self.totalScoreValue.undraw()
        self.instructions.undraw()
        self.replayButton.undraw()


def main():

    game = gameInterface(800, 600)
    game.draw(game.win)
    game.setSelector()
    startRound = True
    while startRound == True:
        score = scoreBoard(game.win)
        score.draw(game.win)
        arrows = 5
        crosses = []
        for trial in range(arrows):
            game.reset()
            angle = game.selection()
            arrow = Arrow(angle[0], angle[1], height=1.73)

            dt = 0.001
            while arrow.getDistance() <= 2.37:
                arrow.update(dt)

            ycoord = (
                game.height // 2
                - ((arrow.getAltitude() - (1.73 + (0.451 / 2))) * 2 * game.height // 3)
                / 0.451
            )

            if ycoord < (game.height // 2 + game.radius + 15) and ycoord > (
                game.height // 2 - game.radius - 15
            ):
                cross = arrowSymbol(graphics.Point(game.width // 2, ycoord))
                crosses.append(cross)
                cross.draw(game.win)
                score.update(cross)
            else:
                score.latestValue.setText("Missed")

            arrows = arrows - 1
            score.arrowsLeft.setText("Arrows left: " + str(arrows))

        ending = gameOver(game.win, score)
        ending.draw()
        while True:
            click = game.win.getMouse()
            if ending.replayButton.contains(click) == True:
                ending.undraw()
                score.undraw()
                for cross in crosses:
                    cross.undraw()
                game.reset()
                break
            else:
                game.win.close()
                startRound = not startRound
                break


if __name__ == "__main__":
    main()
