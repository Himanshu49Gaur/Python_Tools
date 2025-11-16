import turtle
import math

def draw_gear(t, x, y, radius, teeth, color="black"):
    t.penup()
    t.goto(x, y)
    t.pendown()
    t.color(color)
    t.speed(0) # Fastest speed

    t.setheading(0)
    angle_per_tooth = 360 / teeth
    tooth_width_angle = angle_per_tooth / 2.5 # Angle for the top of the tooth
    tooth_gap_angle = angle_per_tooth - tooth_width_angle # Angle for the gap between teeth

    # Outer radius for teeth tips
    outer_radius = radius * 1.1

    # Draw the main gear body (inner circle)
    t.penup()
    t.goto(x + radius, y)
    t.pendown()
    t.circle(radius)

    # Draw the teeth
    t.penup()
    t.goto(x + radius, y)
    t.setheading(90) # Point up to start drawing teeth
    t.forward(radius)
    t.pendown()

    for i in range(teeth):
        # Move to the tip of the tooth
        t.right(tooth_gap_angle / 2)
        t.forward(outer_radius - radius)
        # Draw the top of the tooth
        t.left(90)
        t.circle(outer_radius, tooth_width_angle)
        t.left(90)
        # Move back to the inner circle
        t.forward(outer_radius - radius)
        # Move to the start of the next tooth gap
        t.right(tooth_gap_angle / 2 + tooth_width_angle)

    # Draw a small center hole
    t.penup()
    t.goto(x + radius / 5, y)
    t.pendown()
    t.circle(radius / 5)

def main():
    screen = turtle.Screen()
    screen.setup(width=800, height=600)
    screen.bgcolor("lightblue")
    screen.title("Engineering Design: Interlocking Gears")

    t = turtle.Turtle()
    t.hideturtle()

    # Draw the first gear
    draw_gear(t, -100, 0, 80, 20, "gray")

    # Draw the second interlocked gear
    # Calculate position to interlock properly
    # The distance between centers should be radius1 + radius2
    # And we need to offset based on tooth alignment
    second_gear_x = -100 + (80 + 80) * math.cos(math.radians(90 / 20)) # Adjust based on tooth width
    draw_gear(t, second_gear_x, 0, 80, 20, "darkgray")

    # Draw a third, smaller gear
    draw_gear(t, 150, 100, 50, 15, "black")

    screen.exitonclick()

if __name__ == "__main__":
    main()
