# importing the required modules
import turtle
from math import cos, sin
import time

screen = turtle.Screen()  # creating the screen
screen.bgcolor('black')
screen.tracer(0)  # we'll update manually

sun = turtle.Turtle()  # turtle object for sun
sun.shape('circle')  # shape of sun
sun.color('yellow')  # colour of sun
sun.shapesize(2)  # make sun bigger
sun.penup()


class Planet(turtle.Turtle):
    def __init__(self, name, radius, color):  # initialize function
        super().__init__(shape='circle')
        self.name = name
        self.radius = radius
        self.c = color
        self.color(self.c)
        self.penup()
        # make planets small
        self.shapesize(0.5)
        # start angle (radians)
        self.angle = 0
        # position the planet at its initial orbit location
        self.move()

    def move(self):
        x = self.radius * cos(self.angle)  # Angle in radians
        y = self.radius * sin(self.angle)
        self.goto(sun.xcor() + x, sun.ycor() + y)


# making planets
mercury = Planet("Mercury", 40, 'grey')
venus = Planet("Venus", 80, 'orange')
earth = Planet("Earth", 100, 'blue')
mars = Planet("Mars", 150, 'red')
jupiter = Planet("Jupiter", 180, 'brown')
saturn = Planet("Saturn", 230, 'pink')
uranus = Planet("Uranus", 250, 'lightblue')
neptune = Planet("Neptune", 280, 'black')

# adding planets to a list
myList = [mercury, venus, earth, mars, jupiter, saturn, uranus, neptune]


try:
    while True:  # while statement
        for p in myList:
            p.move()  # moving the elements of the list

        # Increase the angle by small radians
        mercury.angle += 0.05
        venus.angle += 0.03
        earth.angle += 0.01
        mars.angle += 0.007

        jupiter.angle += 0.02
        saturn.angle += 0.018
        uranus.angle += 0.016
        neptune.angle += 0.005

        screen.update()  # updating the screen once per frame
        time.sleep(0.01)  # small delay to control CPU usage / speed
except turtle.Terminator:
    # window was closed; just exit
    pass
    
    