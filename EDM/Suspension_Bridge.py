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
