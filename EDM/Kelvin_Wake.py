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

def main():
    screen = turtle.Screen()
    screen.setup(width=900, height=600)
    screen.bgcolor("darkblue")
    screen.title("Hydrodynamics: Kelvin Wake Pattern")
    screen.tracer(0)

    t = turtle.Turtle()
    t.hideturtle()
    
    boat_x = 300
    boat_y = 0
    
    draw_kelvin_wake(t, boat_x - 40, boat_y) # Start wake from back of boat
    draw_boat(t, boat_x, boat_y)

    # Annotations
    t.penup()
    t.goto(0, 200)
    t.color("white")
    t.write("Kelvin Wake Angle = 19.47°", align="center", font=("Arial", 14, "bold"))
    
    # Draw dashed center line
    t.penup(); t.goto(boat_x, boat_y); t.color("gray"); t.setheading(180)
    for _ in range(20):
        t.pendown(); t.forward(10); t.penup(); t.forward(10)

    screen.update()
    screen.exitonclick()

if __name__ == "__main__":
    main()
