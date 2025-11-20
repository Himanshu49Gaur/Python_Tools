import turtle 

def draw_member(t, x1, y1, x2, y2, thick=3):
    t.penup()
    t.goto(x1, y1)
    t.pendown()
    t.pensize(thick)
    t.goto(x2, y2)
    # Draw joint node
    t.penup()
    t.goto(x2, y2 - 3)
    t.pendown()
    t.circle(3)

ef draw_force_arrow(t, x, y, length, label):
    t.penup()
    t.goto(x, y + length)
    t.pendown()
    t.color("red")
    t.pensize(2)
    t.setheading(270) # Point down
    t.forward(length)
    # Arrow head
    t.left(45)
    t.backward(10)
    t.forward(10)
    t.right(90)
    t.backward(10)
    
    t.penup()
    t.goto(x + 5, y + length / 2)
    t.write(label, font=("Arial", 10, "bold"))

ef main():
    screen = turtle.Screen()
    screen.setup(width=900, height=500)
    screen.bgcolor("white")
    screen.title("Structural Engineering: Warren Truss Analysis")
    screen.tracer(0)

    t = turtle.Turtle()
    t.hideturtle()
    t.color("black")

    start_x = -300
    start_y = 0
    bay_width = 100
    height = 86.6 # equilateral triangle height for side 100 is approx 86.6
    bays = 6

    # Draw Bottom Chord
    t.penup()
    t.goto(start_x, start_y)
    t.pendown()
    t.forward(bay_width * bays)

    # Draw Top Chord
    t.penup()
    t.goto(start_x + bay_width/2, start_y + height)
    t.pendown()
    t.forward(bay_width * (bays - 1))

    # Draw Diagonals and Verticals
    current_x = start_x
    current_y = start_y
    
    for i in range(bays):
        # Upward diagonal
        draw_member(t, current_x, start_y, current_x + bay_width/2, start_y + height)
        # Downward diagonal
        draw_member(t, current_x + bay_width/2, start_y + height, current_x + bay_width, start_y)
        
        current_x += bay_width

    # Draw Supports
    t.penup()
    t.goto(start_x, start_y - 10)
    t.pendown()
    t.setheading(0)
    t.forward(20); t.backward(40); t.forward(20)
    t.right(90); t.forward(10) # Pin support
    
    t.penup()
    t.goto(start_x + bays * bay_width, start_y - 10)
    t.pendown()
    t.circle(5) # Roller support representation

    # Apply Loads (Engineering Simulation aspect)
    draw_force_arrow(t, start_x + bay_width * 1.5, start_y + height + 20, 50, "F1 = 10kN")
    draw_force_arrow(t, start_x + bay_width * 3.5, start_y + height + 20, 70, "F2 = 20kN")

    screen.update()
    screen.exitonclick()

if __name__ == "__main__":
    main()
