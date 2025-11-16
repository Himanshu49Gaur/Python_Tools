import turtle

def draw_tower(t, x, y, height, width, color="darkgray"):
    t.penup()
    t.goto(x - width/2, y)
    t.pendown()
    t.color(color)
    t.pensize(3)
    t.begin_fill()
    t.forward(width)
    t.left(90)
    t.forward(height)
    t.left(90)
    t.forward(width)
    t.left(90)
    t.forward(height)
    t.left(90)
    t.end_fill()

def draw_main_cable(t, start_x, start_y, end_x, end_y, sag_height, segments, color="brown"):
    t.penup()
    t.goto(start_x, start_y)
    t.pendown()
    t.color(color)
    t.pensize(5)

    # Parametric curve for a catenary/parabola-like shape
    for i in range(segments + 1):
        progress = i / segments
        # x_interp: linear interpolation between start_x and end_x
        x_interp = start_x + progress * (end_x - start_x)
        
        # y_interp: parabolic interpolation for sag
        # This creates a downward curve, with max sag at the midpoint
        mid_x = (start_x + end_x) / 2
        
        # A simple parabolic function for the curve
        # y = a(x - h)^2 + k where (h, k) is the vertex (mid_x, lowest_y)
        # Let's approximate the lowest point at the mid_x, sag_height below start_y
        
        # Calculate 'a' such that at mid_x, it's sag_height lower than start_y
        # And at start_x/end_x, it's start_y (relative to the horizontal line between towers)
        
        # Let's simplify: curve from (0,0) to (span,0) with sag at span/2
        # y = -4 * sag_height / span^2 * x * (x - span)
        
        span = end_x - start_x
        relative_x = x_interp - start_x
        
        y_curve_offset = -4 * sag_height / (span * span) * relative_x * (relative_x - span)
        
        # y_position is the start_y minus the curve offset (because sag is downwards)
        y_interp = start_y - y_curve_offset
        
        t.goto(x_interp, y_interp)

def draw_suspender(t, cable_x, cable_y, deck_y, color="black"):
    t.penup()
    t.goto(cable_x, cable_y)
    t.pendown()
    t.color(color)
    t.pensize(1)
    t.goto(cable_x, deck_y)

def main():
    screen = turtle.Screen()
    screen.setup(width=1000, height=600)
    screen.bgcolor("lightcyan")
    screen.title("Engineering Design: Suspension Bridge Structure")
    screen.tracer(0) # Turn off screen updates

    t = turtle.Turtle()
    t.hideturtle()

    # Bridge deck height
    deck_y = -100
    
    # Draw the bridge deck
    t.penup()
    t.goto(-450, deck_y)
    t.pendown()
    t.color("darkslategray")
    t.pensize(10)
    t.forward(900)

    # Draw towers
    tower_height = 250
    tower_width = 30
    draw_tower(t, -300, deck_y, tower_height, tower_width)
    draw_tower(t, 300, deck_y, tower_height, tower_width)

    # Tower tops for cable attachment
    tower1_top_x = -300
    tower1_top_y = deck_y + tower_height
    tower2_top_x = 300
    tower2_top_y = deck_y + tower_height

    # Draw main suspension cable
    sag = 150 # How much the cable sags below the tower tops
    draw_main_cable(t, tower1_top_x, tower1_top_y, tower2_top_x, tower2_top_y, sag, 50, "darkred")

    # Draw suspender cables
    num_suspenders = 20
    span_width = tower2_top_x - tower1_top_x
    for i in range(1, num_suspenders):
        # Calculate cable point for suspender
        cable_x = tower1_top_x + i * span_width / num_suspenders
        
        # Recalculate y based on the main cable's curve function
        relative_x = cable_x - tower1_top_x
        y_curve_offset = -4 * sag / (span_width * span_width) * relative_x * (relative_x - span_width)
        cable_y = tower1_top_y - y_curve_offset
        
        draw_suspender(t, cable_x, cable_y, deck_y, "gray")

    # Draw anchors for main cables (simplified)
    t.penup()
    t.goto(-400, deck_y)
    t.pendown()
    t.color("darkred")
    t.pensize(5)
    t.setheading(135) # Angle towards the tower
    t.forward(100)

    t.penup()
    t.goto(400, deck_y)
    t.pendown()
    t.setheading(45) # Angle towards the tower
    t.forward(100)

    screen.update() # Update the screen once everything is drawn
    screen.exitonclick()

if __name__ == "__main__":
    main()
