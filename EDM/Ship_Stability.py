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

def draw_stability_points(t, x, y, tilt):
    # Center of hull is roughly (x, y - 100)
    # Let's define points relative to the tilted ship frame
    
    rad = math.radians(tilt)
    cos_t = math.cos(rad)
    sin_t = math.sin(rad)
    
    # Center of Gravity G (Fixed on ship)
    # Local coords (0, -80)
    gx = x + (0 * cos_t - (-80) * sin_t)
    gy = y + (0 * sin_t + (-80) * cos_t)
    
    # Original Center of Buoyancy B (Fixed on ship)
    # Local coords (0, -120)
    bx = x + (0 * cos_t - (-120) * sin_t)
    by = y + (0 * sin_t + (-120) * cos_t)
    
    # Shifted Center of Buoyancy B1 (Moves towards the dip)
    # Local coords (40, -110) approx
    b1x = x + (40 * cos_t - (-110) * sin_t)
    b1y = y + (40 * sin_t + (-110) * cos_t)
    
    # Metacenter M (Intersection of centerline and vertical from B1)
    # Local coords (0, -30)
    mx = x + (0 * cos_t - (-30) * sin_t)
    my = y + (0 * sin_t + (-30) * cos_t)

    # Draw Centerline
    t.penup(); t.goto(mx, my); t.pendown()
    t.color("black", "black"); t.pensize(1); t.setheading(-tilt - 90); t.forward(150)
    
    # Draw Vertical Buoyancy Force Line (Up from B1 passing through M)
    t.penup(); t.goto(b1x, b1y); t.pendown()
    t.color("red"); t.setheading(90); t.forward(150) # Straight up
    
    # Draw Gravity Force Line (Down from G)
    t.penup(); t.goto(gx, gy); t.pendown()
    t.color("red"); t.setheading(270); t.forward(80) # Straight down

    # Mark Points
    def dot(px, py, label, c):
        t.penup(); t.goto(px, py-3); t.pendown(); t.color(c); t.begin_fill(); t.circle(4); t.end_fill()
        t.penup(); t.goto(px + 10, py); t.write(label, font=("Arial", 12, "bold"))

    dot(gx, gy, "G", "black")
    dot(b1x, b1y, "B'", "blue")
    dot(mx, my, "M", "green")
    
    # Draw Righting Arm GZ
    # Z is perpendicular projection from G to the B-M line
    # Visual approximation line
    t.penup(); t.goto(gx, gy); t.pendown()
    t.color("purple"); t.pensize(3); t.goto(gx + 35, gy) # Horizontal approx
    t.penup(); t.goto(gx + 10, gy - 15); t.write("GZ (Righting Arm)", font=("Arial", 8, "bold"))
