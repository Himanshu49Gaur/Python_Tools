import turtle

def draw_manometer(t, x, y, height, color):
    # Tube
    t.penup()
    t.goto(x, y)
    t.pensize(3)
    t.color("black")
    t.pendown()
    t.setheading(90)
    t.forward(150)
    
    # Liquid level
    t.penup()
    t.goto(x, y)
    t.color(color)
    t.pensize(6)
    t.pendown()
    t.forward(height)
    
    # Meniscus
    t.color("black")
    t.pensize(1)
    t.circle(3)
