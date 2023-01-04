"""
Author: Prof. Davis
Date: 22/04/2022
Citations and Acknowledgments:
    This code was provided by Prof. Davis
    This code was edited by Fabian Gabriel
"""
import graphics

class Button:
    def __init__(self, p1, p2, label=""):
        """Create a button.

        Parameters:
                p1:   the top left point
                p2:   the bottom right point
                text: a string object, defaults to ""
        """
        assert p1.getX() < p2.getX()
        assert p1.getY() < p2.getY()

        self.rect = graphics.Rectangle(p1, p2)
        self.text = graphics.Text(self.rect.getCenter(), label)

        self.drawn = False
        self.win = None
        self.image = None

    def draw(self, win):
        """Draw this button in the given GraphWin."""
        self.drawn = True
        self.win = win
        self.rect.draw(win)
        self.text.draw(win)
        if self.image:
            self.image.draw()

    def undraw(self):
        """Undraw this button."""
        self.rect.undraw()
        self.text.undraw()
        if self.image:
            self.image.undraw()
        self.drawn = False

    def setFill(self, color):
        """Set the button fill color."""
        self.rect.setFill(color)

    def setOutline(self, color):
        """Set the button outline color"""
        self.rect.setOutline(color)

    def setWidth(self, width):
        """Set the button outline width"""
        self.rect.setWidth(width)

    def setTextColor(self, color):
        """Set the button text color."""
        self.text.setTextColor(color)

    def setText(self, label):
        """Set the button text."""
        self.text.setText(label)

    def setTextSize(self, size):
        """Set the button text size."""
        self.text.setSize(size)

    def setImage(self, filename):
        """Set the button image to one loaded from the given filename."""
        if self.image and self.drawn:
            self.image.undraw()
        self.image = graphics.Image(self.getCenter(), filename)
        if self.drawn:
            self.image.draw(self.win)

    def getP1(self):
        """Get a point representing the upper left corner of the button."""
        return self.rect.getP1()

    def getP2(self):
        """Get a point representing the lower right corner of the button."""
        return self.rect.getP2()

    def getCenter(self):
        """Get a point representing the center of the button."""
        return self.rect.getCenter()

    def getText(self):
        """Get the text of the button."""
        return self.text.getText()

    def getImage(self):
        """Get a copy of the button image, or None if the button has no image."""
        if self.image:
            return self.image.clone()
        return None

    def contains(self, p):
        """Determine if the point p is contained within this button."""
        return (
            p.getX() > self.rect.getP1().getX()
            and p.getY() > self.rect.getP1().getY()
            and p.getX() < self.rect.getP2().getX()
            and p.getY() < self.rect.getP2().getY()
        )