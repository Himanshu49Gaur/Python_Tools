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

def main():
    screen = turtle.Screen()
    screen.setup(width=1000, height=800)
    screen.bgcolor("white")
    screen.title("Engineering Design: Isometric Grid with Boxes")
    screen.tracer(0) # Turn off screen updates for faster drawing
    
    t = turtle.Turtle()
    t.hideturtle()
    t.speed(0)

    # Draw an isometric grid (simplified version)
    grid_spacing = 50
    grid_lines = 8
    grid_length = grid_spacing * grid_lines
    
    # Start drawing from a point that puts the grid roughly centered
    grid_start_x = -300
    grid_start_y = -150

    # Draw lines for two directions of the isometric grid
    t.color("lightgray")
    t.pensize(1)
    
    # Lines parallel to the x-axis (0 degrees)
    for i in range(grid_lines + 1):
        t.penup()
        t.goto(grid_start_x, grid_start_y + i * grid_spacing)
        t.pendown()
        t.setheading(0)
        t.forward(grid_length)

    # Lines at 60 degrees from the x-axis
    for i in range(grid_lines + 1):
        t.penup()
        # Start points need to be adjusted to form the grid
        start_point_x = grid_start_x + i * grid_spacing * math.cos(math.radians(60))
        start_point_y = grid_start_y + i * grid_spacing * math.sin(math.radians(60))
        t.goto(start_point_x, start_point_y)
        t.pendown()
        t.setheading(60)
        t.forward(grid_length)

    # Lines at 120 degrees (or -60 degrees from horizontal for the other diagonal)
    for i in range(grid_lines + 1):
        t.penup()
        # This one is a bit trickier to align perfectly for a full grid without a proper matrix transform
        # For simplicity, we can draw from the end of the 0-degree lines
        t.goto(grid_start_x + grid_length, grid_start_y + i * grid_spacing)
        t.pendown()
        t.setheading(120)
        t.forward(grid_length)


    # Draw some isometric cubes on the grid
    cube_size = grid_spacing
    
    draw_isometric_cube(t, grid_start_x + grid_spacing, grid_start_y, cube_size, "red")
    draw_isometric_cube(t, grid_start_x + 2 * grid_spacing, grid_start_y, cube_size, "orange")
    
    # Stacked cubes
    draw_isometric_cube(t, grid_start_x + 3 * grid_spacing, grid_start_y, cube_size, "purple")
    # To draw on top, the base of the new cube starts at the top-left corner of the previous
    # This requires more precise calculations of isometric points
    # For now, let's just place them adjacent for simplicity
    
    # A simplified way to draw a cube on top of another
    # Start point for the top cube would be x_base, y_base + cube_size * math.sin(math.radians(60))
    # or x_base, y_base + size (vertically stacked, which is not isometric)
    # For isometric stack, need to calculate the actual top-left point of the base cube.
    
    # Let's draw some boxes on different "levels" of the isometric plane
    draw_isometric_cube(t, grid_start_x + grid_spacing * 4, grid_start_y + grid_spacing, cube_size, "green")
    draw_isometric_cube(t, grid_start_x + grid_spacing * 5, grid_start_y + grid_spacing, cube_size, "darkblue")

    screen.update() # Update the screen once everything is drawn
    screen.exitonclick()

if __name__ == "__main__":
    main()
