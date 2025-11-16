import turtle
import random

def draw_trace(t, start_x, start_y, length, color="green"):
    t.penup()
    t.goto(start_x, start_y)
    t.pendown()
    t.color(color)
    t.pensize(random.randint(1, 3)) # Vary line thickness

    directions = [0, 90, 180, 270] # Right, Up, Left, Down
    current_direction = random.choice(directions)
    t.setheading(current_direction)

    for _ in range(random.randint(5, 15)): # Draw several segments
        turn_angle = random.choice([-90, 0, 90]) # Left, Straight, Right
        t.right(turn_angle)
        
        segment_length = random.randint(length // 4, length)
        t.forward(segment_length)
        
        # Add small "pads" or "components" sometimes
        if random.random() < 0.1:
            draw_component_pad(t)

def draw_component_pad(t):
    pad_size = random.randint(2, 5)
    t.dot(pad_size * 2, "gold") # A gold-colored pad
    # Optionally draw a small square
    t.fillcolor("gold")
    t.begin_fill()
    t.circle(pad_size)
    t.end_fill()

def main():
    screen = turtle.Screen()
    screen.setup(width=900, height=700)
    screen.bgcolor("darkgreen") # PCB substrate color
    screen.title("Engineering Design: Circuit Board Traces")
    screen.tracer(0) # Turn off screen updates for faster drawing

    t = turtle.Turtle()
    t.hideturtle()

    num_traces = 50
    trace_length_max = 100

    # Draw various traces across the board
    for _ in range(num_traces):
        start_x = random.randint(-400, 400)
        start_y = random.randint(-300, 300)
        draw_trace(t, start_x, start_y, trace_length_max, random.choice(["lightgreen", "yellow", "orange", "cyan"]))

    # Draw some larger "chip" outlines or components
    t.penup()
    t.goto(-300, 200)
    t.pendown()
    t.color("black")
    t.pensize(5)
    t.setheading(0)
    for _ in range(2):
        t.forward(100)
        t.right(90)
        t.forward(60)
        t.right(90)

    t.penup()
    t.goto(200, -150)
    t.pendown()
    t.color("black")
    t.pensize(5)
    t.setheading(0)
    for _ in range(2):
        t.forward(80)
        t.right(90)
        t.forward(80)
        t.right(90)

    screen.update() # Update the screen once everything is drawn
    screen.exitonclick()

if __name__ == "__main__":
    main()
