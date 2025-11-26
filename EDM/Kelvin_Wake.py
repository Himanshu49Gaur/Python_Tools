import turtle 
import math

def draw_boat(t, x, y):
    t.penup(); t.goto(x, y); t.pendown()
    t.color("black"); t.fillcolor("brown"); t.begin_fill()
    t.setheading(0)
    t.forward(40)
    t.left(150); t.forward(50)
    t.left(60); t.forward(50)
    t.end_fill()
