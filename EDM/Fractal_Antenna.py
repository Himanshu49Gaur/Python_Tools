import turtle
import random

def draw_fractal_tree(t, branch_len, angle, level):
    if level > 0:
        t.pensize(level * 1.5) # Thicker branches at lower levels
        if level <= 2:
            t.color("forestgreen") # Leaves/smaller branches
        else:
            t.color("saddlebrown") # Trunk/larger branches

        t.forward(branch_len)
        t.right(angle)
        draw_fractal_tree(t, branch_len * 0.75, angle, level - 1)
        t.left(angle * 2)
        draw_fractal_tree(t, branch_len * 0.75, angle, level - 1)
        t.right(angle)
        t.backward(branch_len) # Go back to the joint

def main():
    screen = turtle.Screen()
    screen.setup(width=800, height=800)
    screen.bgcolor("skyblue")
    screen.title("Engineering Design: Fractal Antenna/Tree")
    screen.tracer(0) # Turn off screen updates

    t = turtle.Turtle()
    t.hideturtle()
    t.speed(0) # Fastest speed

    t.penup()
    t.goto(0, -250)
    t.pendown()
    t.left(90) # Point upwards

    initial_branch_length = 150
    split_angle = 30 # Angle for branching
    recursion_level = 6

    draw_fractal_tree(t, initial_branch_length, split_angle, recursion_level)

    # Optionally draw a "ground" line
    t.penup()
    t.goto(-400, -250)
    t.pendown()
    t.pensize(5)
    t.color("darkgreen")
    t.forward(800)

    screen.update() # Update the screen once everything is drawn
    screen.exitonclick()

if __name__ == "__main__":
    main()
