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
