import turtle

def draw_manometer(t, x, y, height, color):
    # Tube
    t.penup()
    t.goto(x, y)
    t.pensize(3)
    t.color("black")
    t.pendown()
    t.setheading(90)
    t.forward(150)
    
    # Liquid level
    t.penup()
    t.goto(x, y)
    t.color(color)
    t.pensize(6)
    t.pendown()
    t.forward(height)
    
    # Meniscus
    t.color("black")
    t.pensize(1)
    t.circle(3)

def main():
    screen = turtle.Screen()
    screen.setup(width=800, height=500)
    screen.bgcolor("white")
    screen.title("Fluid Mechanics: Venturi Effect")
    screen.tracer(0)

    t = turtle.Turtle()
    t.hideturtle()

    # Define pipe shape coordinates
    inlet_y = 60
    throat_y = 20
    length = 600
    start_x = -300
    
    # 1. Draw Pipe Walls
    t.penup()
    t.goto(start_x, inlet_y)
    t.pendown()
    t.pensize(3)
    t.color("black")
    
    # Top Wall
    t.goto(start_x + 150, inlet_y) # Inlet section
    t.goto(start_x + 250, throat_y) # Converging
    t.goto(start_x + 350, throat_y) # Throat section
    t.goto(start_x + 450, inlet_y) # Diverging
    t.goto(start_x + 600, inlet_y) # Outlet section
    
    # Bottom Wall
    t.penup()
    t.goto(start_x, -inlet_y)
    t.pendown()
    t.goto(start_x + 150, -inlet_y)
    t.goto(start_x + 250, -throat_y)
    t.goto(start_x + 350, -throat_y)
    t.goto(start_x + 450, -inlet_y)
    t.goto(start_x + 600, -inlet_y)

    # 2. Draw Streamlines (Blue Flow)
    t.pensize(1)
    t.color("blue")
    for i in range(-2, 3):
        offset = i * 15
        t.penup()
        t.goto(start_x, offset)
        t.pendown()
        # Simple interpolation for visual effect
        t.goto(start_x + 150, offset)
        t.goto(start_x + 250, offset * (throat_y/inlet_y))
        t.goto(start_x + 350, offset * (throat_y/inlet_y))
        t.goto(start_x + 450, offset)
        t.goto(start_x + 600, offset)

    # 3. Draw Manometers (Pressure Gauges)
    # Inlet Pressure (High)
    draw_manometer(t, start_x + 100, inlet_y, 100, "cyan")
    # Throat Pressure (Low - Velocity is high)
    draw_manometer(t, start_x + 300, throat_y, 30, "cyan")
    # Outlet Pressure (Recovered but slightly lower due to friction)
    draw_manometer(t, start_x + 550, inlet_y, 80, "cyan")

    # Annotations
    t.penup(); t.goto(start_x + 100, -100); t.color("red"); t.write("High Pressure\nLow Velocity", align="center", font=("Arial", 10, "bold"))
    t.penup(); t.goto(start_x + 300, -80); t.color("red"); t.write("Low Pressure\nHigh Velocity", align="center", font=("Arial", 10, "bold"))

    screen.update()
    screen.exitonclick()

if __name__ == "__main__":
    main()
