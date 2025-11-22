import math
import turtle

def draw_orbit(t, radius, color, name, speed_label):
    t.penup()
    t.goto(0, -radius)
    t.setheading(0)
    t.pendown()
    t.color(color)
    t.circle(radius)
    
    # Draw Planet
    t.penup()
    t.goto(radius, 0)
    t.pendown()
    t.begin_fill()
    t.circle(10)
    t.end_fill()
    
    t.penup()
    t.goto(radius + 15, 0)
    t.write(name, font=("Arial", 10, "bold"))
    
    # Velocity Vector
    t.goto(radius, 0)
    t.pendown()
    t.pensize(2)
    t.setheading(90)
    t.forward(40)
    t.write(f"  {speed_label}", font=("Arial", 8, "normal"))
