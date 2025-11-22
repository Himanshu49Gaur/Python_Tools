import turtle 
import math

def draw_hexagon(t, x, y, size, color):
    t.penup()
    t.goto(x, y)
    t.pendown()
    t.color("black", color)
    t.pensize(1)
    t.begin_fill()
    for _ in range(6):
        t.forward(size)
        t.left(60)
    t.end_fill()
