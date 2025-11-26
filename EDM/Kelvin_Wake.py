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

def draw_kelvin_wake(t, x, y):
    t.pensize(1)
    
    # 1. The Cusp Lines (The V shape envelope)
    # Angle is asin(1/3) = approx 19.47 degrees
    angle = 19.47
    
    t.color("blue")
    t.penup(); t.goto(x, y); t.pendown()
    t.setheading(180 + angle)
    t.forward(400)
    
    t.penup(); t.goto(x, y); t.pendown()
    t.setheading(180 - angle)
    t.forward(400)
    
    # 2. Transverse and Divergent Waves
    # This is a simplified geometric representation using parametric points
    t.color("white")
    
    # Draw several "cusps" along the wake
    for i in range(1, 15):
        dist = i * 25
        
        # Upper arm wave crests (Curved)
        t.penup()
        start_x = x - dist * math.cos(math.radians(angle))
        start_y = y + dist * math.sin(math.radians(angle))
        t.goto(start_x, start_y)
        t.setheading(0)
        t.pendown()
        t.circle(-dist/2, 60) # Approximating the curve of the wake components
        
        # Lower arm wave crests
        t.penup()
        start_x_low = x - dist * math.cos(math.radians(angle))
        start_y_low = y - dist * math.sin(math.radians(angle))
        t.goto(start_x_low, start_y_low)
        t.setheading(0)
        t.pendown()
        t.circle(dist/2, 60)
