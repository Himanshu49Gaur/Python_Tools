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
