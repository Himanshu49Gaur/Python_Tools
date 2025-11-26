import turtle
import random

def draw_destroyer_outline(t):
    t.penup()
    t.goto(-300, 0)
    t.pendown()
    t.color("black")
    t.pensize(3)
    
    # Hull
    t.begin_fill()
    t.fillcolor("gray")
    t.forward(50) # Stern
    t.setheading(30)
    t.forward(40) # Deck rise
    t.setheading(0)
    t.forward(400) # Deck
    t.setheading(-45)
    t.forward(60) # Bow
    t.setheading(180)
    t.forward(500) # Bottom
    t.setheading(90)
    t.forward(42) # Stern vertical
    t.end_fill()
    
    # Superstructure
    t.penup(); t.goto(-100, 40); t.setheading(0); t.pendown()
    t.begin_fill(); t.forward(150); t.left(90); t.forward(40); t.left(90); t.forward(150); t.left(90); t.forward(40); t.end_fill()
    
    # Funnels
    t.penup(); t.goto(-60, 80); t.setheading(0); t.pendown(); 
    t.begin_fill(); t.left(80); t.forward(40); t.right(80); t.forward(20); t.right(100); t.forward(40); t.end_fill()
    t.penup(); t.goto(-10, 80); t.setheading(0); t.pendown(); 
    t.begin_fill(); t.left(80); t.forward(40); t.right(80); t.forward(20); t.right(100); t.forward(40); t.end_fill()
