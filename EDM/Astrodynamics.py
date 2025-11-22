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

def main():
    screen = turtle.Screen()
    screen.setup(width=800, height=800)
    screen.bgcolor("black") # Space background
    screen.title("Astrodynamics: Hohmann Transfer Orbit")
    screen.tracer(0)

    t = turtle.Turtle()
    t.hideturtle()

    # Sun
    t.penup(); t.goto(0, -20); t.pendown()
    t.color("yellow"); t.begin_fill(); t.circle(20); t.end_fill()

    r1 = 150 # Inner Orbit (Earth)
    r2 = 300 # Outer Orbit (Mars)

    # Draw Circular Orbits
    draw_orbit(t, r1, "blue", "Earth (Start)", "V1")
    draw_orbit(t, r2, "red", "Mars (Target)", "V2")

    # Draw Transfer Ellipse
    # Semi-major axis a = (r1 + r2) / 2
    # Center of ellipse is offset from Sun
    a = (r1 + r2) / 2
    c = a - r1 # linear eccentricity distance
    
    t.penup()
    t.color("green")
    t.pensize(2)
    
    # We draw the ellipse mathematically
    # Center of ellipse is at (-c, 0) assuming periapsis is at right (r1, 0)
    # Actually, let's put periapsis at (r1, 0) and apoapsis at (-r2, 0)
    # So center is at (r1 - r2) / 2
    
    center_x = (r1 - r2) / 2
    b = math.sqrt(a**2 - center_x**2) # Semi-minor axis
    
    # Draw dashed transfer path
    t.penup()
    # Start at Periapsis (Earth)
    t.goto(r1, 0) 
    t.pendown()
    
    steps = 100
    for i in range(steps // 2 + 1): # Only draw half orbit (transfer phase)
        theta = math.pi * (i / (steps/2))
        # Ellipse parameterization
        x = center_x + a * math.cos(theta) # Note: Adjust phase if needed
        # Let's adjust logic: Periapsis at right side (angle 0 relative to ellipse center)
        # At theta=0, x = center_x + a = (r1-r2)/2 + (r1+r2)/2 = r1. Correct.
        y = b * math.sin(theta)
        
        if i % 2 == 0: # Dash effect
            t.pendown()
        else:
            t.penup()
        t.goto(x, y)

    # Draw Delta-V burns labels
    t.penup()
    t.goto(r1 + 20, -20)
    t.color("lightgreen")
    t.write("ΔV1 (Burn to Ellipse)", font=("Arial", 10, "bold"))
    
    t.goto(-r2 - 20, 20)
    t.write("ΔV2 (Burn to Circularize)", align="right", font=("Arial", 10, "bold"))

    screen.update()
    screen.exitonclick()

if __name__ == "__main__":
    main()
