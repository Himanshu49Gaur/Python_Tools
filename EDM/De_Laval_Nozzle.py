import turtle 
import math 

def draw_nozzle_curve(t, start_x, start_y, length, throat_y, exit_y, mirror=False):
    t.penup()
    t.goto(start_x, start_y)
    t.pendown()
    t.color("white")
    t.pensize(3)
    
    steps = 50
    dx = length / steps
    
    # Using a cosine function to approximate the bell nozzle shape
    for i in range(steps + 1):
        x = start_x + i * dx
        progress = i / steps
        
        # Interpolate radius: Start -> Throat -> Exit
        # We use a composite curve logic here
        if progress < 0.3: # Converging section
            local_progress = progress / 0.3
            # Curve down to throat
            y = start_y - (start_y - throat_y) * math.sin(local_progress * math.pi / 2)
        else: # Diverging section
            local_progress = (progress - 0.3) / 0.7
            # Curve out to exit
            y = throat_y + (exit_y - throat_y) * (1 - math.cos(local_progress * math.pi / 2))
            
        if mirror:
            t.goto(x, -y)
        else:
            t.goto(x, y)

def draw_shock_diamonds(t, start_x, count, size):
    t.pensize(2)
    x = start_x
    for i in range(count):
        # Draw the diamond shape
        t.penup()
        t.goto(x, 0)
        t.color("cyan", "lightblue")
        t.pendown()
        t.begin_fill()
        t.goto(x + size/2, size/3)
        t.goto(x + size, 0)
        t.goto(x + size/2, -size/3)
        t.goto(x, 0)
        t.end_fill()
        x += size

def main():
    screen = turtle.Screen()
    screen.setup(width=900, height=500)
    screen.bgcolor("black")
    screen.title("Propulsion: De Laval Nozzle with Shock Diamonds")
    screen.tracer(0)

    t = turtle.Turtle()
    t.hideturtle()

    # Parameters
    chamber_x = -300
    chamber_radius = 100
    nozzle_len = 300
    throat_radius = 40
    exit_radius = 90

    # Draw Combustion Chamber
    t.penup()
    t.goto(chamber_x - 100, chamber_radius)
    t.pendown()
    t.color("gray")
    t.begin_fill()
    t.goto(chamber_x, chamber_radius)
    t.goto(chamber_x, -chamber_radius)
    t.goto(chamber_x - 100, -chamber_radius)
    t.goto(chamber_x - 100, chamber_radius)
    t.end_fill()

    # Draw Nozzle Walls
    draw_nozzle_curve(t, chamber_x, chamber_radius, nozzle_len, throat_radius, exit_radius, mirror=False)
    draw_nozzle_curve(t, chamber_x, chamber_radius, nozzle_len, throat_radius, exit_radius, mirror=True)

    # Draw Exhaust Plume Boundary (dashed)
    t.color("yellow")
    t.pensize(1)
    t.penup(); t.goto(chamber_x + nozzle_len, exit_radius); t.pendown()
    t.goto(chamber_x + nozzle_len + 400, 20)
    t.penup(); t.goto(chamber_x + nozzle_len, -exit_radius); t.pendown()
    t.goto(chamber_x + nozzle_len + 400, -20)

    # Draw Shock Diamonds (Mach Disks)
    draw_shock_diamonds(t, chamber_x + nozzle_len, 6, 60)

    # Text Labels
    t.penup()
    t.color("white")
    t.goto(chamber_x - 50, 120); t.write("Combustion Chamber", align="center", font=("Arial", 10, "bold"))
    t.goto(chamber_x + nozzle_len * 0.3, 60); t.write("Throat (M=1)", align="center", font=("Arial", 10, "bold"))
    t.goto(chamber_x + nozzle_len, 110); t.write("Exit (M>1)", align="center", font=("Arial", 10, "bold"))
    t.goto(chamber_x + nozzle_len + 150, -80); t.write("Shock Diamonds", align="center", font=("Arial", 10, "italic"))

    screen.update()
    screen.exitonclick()

if __name__ == "__main__":
    main()
