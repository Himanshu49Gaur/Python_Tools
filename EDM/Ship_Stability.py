import turtle 
import math

def draw_hull(t, x, y, tilt_angle):
    t.penup()
    t.goto(x, y)
    t.setheading(-tilt_angle) # Tilt the coordinate system
    
    # Draw U-shaped hull
    t.pendown()
    t.color("black")
    t.pensize(3)
    t.fillcolor("lightgray")
    t.begin_fill()
    t.forward(100) # Right deck
    t.right(90)
    t.circle(-100, 180) # Bottom hull
    t.right(90)
    t.forward(100) # Left deck
    t.end_fill()
    
    # Draw Waterline (Horizontal relative to world, tilted relative to ship)
    t.penup()
    # Calculate start point of waterline based on tilt
    t.goto(x - 120, y - 50) 
    t.setheading(0) # Water is always flat
    t.color("blue")
    t.pensize(2)
    t.pendown()
    t.forward(240)
    t.penup()
    t.goto(x + 130, y - 50); t.write("Waterline", font=("Arial", 10, "italic"))
