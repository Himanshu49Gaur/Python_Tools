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
