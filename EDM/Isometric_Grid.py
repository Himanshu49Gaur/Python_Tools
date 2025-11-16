import turtle
import math

def draw_isometric_line(t, length, angle):
    t.setheading(angle)
    t.forward(length)

def draw_isometric_cube(t, x, y, size, color="blue"):
    t.penup()
    t.goto(x, y)
    t.pendown()
    t.color(color)
    t.pensize(2)

    # Front face (bottom left corner at (x,y))
    # Bottom edge
    draw_isometric_line(t, size, 0)
    # Right edge
    draw_isometric_line(t, size, 60)
    # Top edge
    draw_isometric_line(t, size, 180)
    # Left edge
    draw_isometric_line(t, size, 240) # Should be -120 or 240
    
    # Top face
    t.penup()
    t.goto(x + size, y) # Start at front-right corner
    t.pendown()
    draw_isometric_line(t, size, 120)
    draw_isometric_line(t, size, 180) # Back edge of top face

    # Right face
    t.penup()
    t.goto(x + size, y) # Start at front-right corner
    t.pendown()
    draw_isometric_line(t, size, 60) # Top edge of right face
    t.setheading(300) # Should be -60 or 300
    t.forward(size) # Back edge of right face

def draw_isometric_grid(t, start_x, start_y, grid_size, num_lines, line_length):
    t.color("gray")
    t.pensize(1)

    # Draw lines at 0 degrees
    for i in range(num_lines):
        t.penup()
        t.goto(start_x, start_y + i * grid_size)
        t.pendown()
        draw_isometric_line(t, line_length, 0)

    # Draw lines at 60 degrees
    for i in range(num_lines):
        t.penup()
        t.goto(start_x + i * grid_size * math.cos(math.radians(60)), start_y + i * grid_size * math.sin(math.radians(60)))
        t.pendown()
        draw_isometric_line(t, line_length, 60)

    # Draw lines at 120 degrees
    for i in range(num_lines):
        t.penup()
        t.goto(start_x + i * grid_size * math.cos(math.radians(120)) + line_length * math.cos(math.radians(0)), 
               start_y + i * grid_size * math.sin(math.radians(120)) + line_length * math.sin(math.radians(0)))
        t.pendown()
        draw_isometric_line(t, line_length, 120)
