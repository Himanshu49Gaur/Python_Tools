import turtle
import math

def draw_piston_assembly(t, crank_x, crank_y, crank_r, rod_l, angle):
    # Calculate joints
    # Crank pin position
    pin_x = crank_x + crank_r * math.cos(math.radians(angle))
    pin_y = crank_y + crank_r * math.sin(math.radians(angle))
    
    # Piston pin position (constrained to y = crank_y)
    # Use law of cosines / pythagoras logic to find x of piston
    # (pin_x - piston_x)^2 + (pin_y - crank_y)^2 = rod_l^2
    # piston_x = pin_x + sqrt(rod_l^2 - (pin_y - crank_y)^2)
    
    dy = pin_y - crank_y
    dx = math.sqrt(rod_l**2 - dy**2)
    piston_x = pin_x + dx
    piston_y = crank_y

    t.color("black")
    t.pensize(3)

    # Draw Crank
    t.penup(); t.goto(crank_x, crank_y); t.pendown()
    t.goto(pin_x, pin_y)
    
    # Draw Connecting Rod
    t.color("darkgray")
    t.pensize(5)
    t.goto(piston_x, piston_y)

    # Draw Piston (Box)
    t.penup()
    t.goto(piston_x - 20, piston_y - 15)
    t.pendown()
    t.color("black", "lightgray")
    t.begin_fill()
    for _ in range(2):
        t.forward(40)
        t.left(90)
        t.forward(30)
        t.left(90)
    t.end_fill()

    # Draw Cylinder Walls
    t.penup()
    t.pensize(2)
    t.color("black")
    t.goto(crank_x + crank_r + 10, crank_y + 16)
    t.pendown(); t.forward(rod_l + 60)
    t.penup()
    t.goto(crank_x + crank_r + 10, crank_y - 16)
    t.pendown(); t.forward(rod_l + 60)
    
    # Draw Crank Circle (Path)
    t.penup(); t.goto(crank_x, crank_y - crank_r); t.pendown()
    t.color("lightgray"); t.pensize(1); t.circle(crank_r)

def main():
    screen = turtle.Screen()
    screen.setup(width=800, height=400)
    screen.title("Kinematics: Crank-Slider Mechanism")
    screen.tracer(0)

    t = turtle.Turtle()
    t.hideturtle()

    crank_radius = 60
    rod_length = 180
    
    # Draw a few "ghosted" frames to imply motion
    angles = [0, 45, 90, 135, 180]
    
    # Draw main assembly at 45 degrees
    draw_piston_assembly(t, -100, 0, crank_radius, rod_length, 45)
    
    # Annotations
    t.penup(); t.goto(-110, -80); t.color("black"); t.write("Crank", font=("Arial", 10, "normal"))
    t.penup(); t.goto(0, 50); t.write("Connecting Rod", font=("Arial", 10, "normal"))
    t.penup(); t.goto(150, 30); t.write("Piston", font=("Arial", 10, "normal"))

    screen.update()
    screen.exitonclick()

if __name__ == "__main__":
    main()
