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

ef draw_force_arrow(t, x, y, length, label):
    t.penup()
    t.goto(x, y + length)
    t.pendown()
    t.color("red")
    t.pensize(2)
    t.setheading(270) # Point down
    t.forward(length)
    # Arrow head
    t.left(45)
    t.backward(10)
    t.forward(10)
    t.right(90)
    t.backward(10)
    
    t.penup()
    t.goto(x + 5, y + length / 2)
    t.write(label, font=("Arial", 10, "bold"))
