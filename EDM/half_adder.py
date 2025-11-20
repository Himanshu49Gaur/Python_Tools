import turtle

def draw_and_gate(t, x, y, scale=1):
    t.penup()
    t.goto(x, y) # Center of the flat back
    t.setheading(0)
    t.pensize(2)
    t.color("black")
    
    # Draw Body
    t.penup()
    t.goto(x, y + 20 * scale) # Top left
    t.pendown()
    t.forward(30 * scale) # Top line
    t.circle(-20 * scale, 180) # Front Curve (semicircle radius 20)
    t.forward(30 * scale) # Bottom line
    t.left(90)
    t.forward(40 * scale) # Back line (closes the gate)
    
    # Inputs (A and B)
    t.penup()
    t.goto(x, y + 10 * scale); t.setheading(180); t.pendown(); t.forward(20 * scale) # Top Input
    t.penup()
    t.goto(x, y - 10 * scale); t.setheading(180); t.pendown(); t.forward(20 * scale) # Bottom Input
    
    # Output
    t.penup()
    t.goto(x + 50 * scale, y); t.setheading(0); t.pendown(); t.forward(20 * scale) # Output line
