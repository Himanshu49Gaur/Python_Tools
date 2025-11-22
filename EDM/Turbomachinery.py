import turtle 

def draw_blade_row(t, x, y_start, y_end, width, color):
    t.color(color)
    t.pensize(1)
    count = 4
    step = (y_end - y_start) / count
    
    t.penup()
    t.goto(x, y_start)
    t.setheading(90)
    
    for i in range(count):
        t.penup()
        t.goto(x, y_start + i*step)
        t.pendown()
        # Draw simple airfoil shape
        t.begin_fill()
        t.goto(x + width, y_start + i*step + step/2)
        t.goto(x, y_start + i*step + step)
        t.goto(x, y_start + i*step)
        t.end_fill()
        
        # Mirror bottom
        t.penup()
        t.goto(x, -(y_start + i*step))
        t.pendown()
        t.begin_fill()
        t.goto(x + width, -(y_start + i*step + step/2))
        t.goto(x, -(y_start + i*step + step))
        t.goto(x, -(y_start + i*step))
        t.end_fill()
