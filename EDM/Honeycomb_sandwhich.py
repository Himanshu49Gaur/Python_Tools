import turtle 
import math

def draw_hexagon(t, x, y, size, color):
    t.penup()
    t.goto(x, y)
    t.pendown()
    t.color("black", color)
    t.pensize(1)
    t.begin_fill()
    for _ in range(6):
        t.forward(size)
        t.left(60)
    t.end_fill()

def main():
    screen = turtle.Screen()
    screen.setup(width=800, height=600)
    screen.bgcolor("white")
    screen.title("Structures: Composite Honeycomb Panel")
    screen.tracer(0)

    t = turtle.Turtle()
    t.hideturtle()

    hex_size = 30
    # Geometry calculation for tessellation
    hex_width = 2 * hex_size * math.cos(math.radians(30)) # distance between parallel sides? No.
    # Horizontal distance between centers:
    h_dist = 3 * hex_size
    # Vertical distance between centers:
    v_dist = hex_size * math.sqrt(3)

    start_x = -300
    start_y = -100
    rows = 5
    cols = 10

    # Draw Top Face Sheet (Peeling up)
    t.penup(); t.goto(start_x - 20, start_y + rows*v_dist + 40); t.pendown()
    t.color("black", "lightgray"); t.begin_fill()
    t.goto(start_x + 400, start_y + rows*v_dist + 150) # Peeling corner
    t.goto(start_x + 600, start_y + rows*v_dist + 20)
    t.goto(start_x - 20, start_y + rows*v_dist + 20)
    t.end_fill()
    t.penup(); t.goto(start_x, start_y + rows*v_dist + 60); t.color("black"); t.write("Carbon Fiber Face Sheet", font=("Arial", 12, "bold"))

    # Draw Honeycomb Core
    for r in range(rows):
        for c in range(cols):
            x = start_x + c * (1.5 * hex_size)
            y = start_y + r * v_dist
            
            if c % 2 == 1:
                y += v_dist / 2
            
            draw_hexagon(t, x, y, hex_size, "gold")

    # Draw Bottom Face Sheet
    t.penup(); t.goto(start_x - 20, start_y - 20); t.pendown()
    t.color("black", "gray"); t.begin_fill()
    t.setheading(0)
    for _ in range(2):
        t.forward(620)
        t.right(90)
        t.forward(20)
        t.right(90)
    t.end_fill()
    
    # Labels
    t.penup()
    t.goto(start_x + 200, start_y + 50)
    t.color("black")
    t.write("Aluminum/Nomex Core", font=("Arial", 12, "bold"))

    screen.update()
    screen.exitonclick()

if __name__ == "__main__":
    main()
