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

def draw_xor_gate(t, x, y, scale=1):
    t.penup()
    t.goto(x, y)
    t.setheading(0)
    t.pensize(2)
    t.color("black")

    # 1. Draw the Shield (Front part)
    t.penup()
    t.goto(x - 5 * scale, y + 20 * scale) # Start top-left of body
    t.pendown()
    t.setheading(0)
    # Top curve moving down-right
    t.circle(-50 * scale, 40) 
    # Jump to bottom to draw bottom curve up-right
    t.penup()
    t.goto(x - 5 * scale, y - 20 * scale)
    t.setheading(0)
    t.pendown()
    t.circle(50 * scale, 40)
    
    # 2. Draw the Curved Back (Body)
    t.penup()
    t.goto(x - 5 * scale, y + 20 * scale)
    t.setheading(290)
    t.pendown()
    t.circle(55 * scale, 40) # Inner back curve

    # 3. Draw the Separation Line (The XOR arc)
    t.penup()
    t.goto(x - 12 * scale, y + 22 * scale)
    t.setheading(290)
    t.pendown()
    t.circle(55 * scale, 42)

    # Inputs (Must pass through the gap)
    t.penup()
    t.goto(x - 5 * scale, y + 10 * scale); t.setheading(180); t.pendown(); t.forward(15 * scale) # Top Input
    t.penup()
    t.goto(x - 5 * scale, y - 10 * scale); t.setheading(180); t.pendown(); t.forward(15 * scale) # Bottom Input

    # Output
    t.penup()
    t.goto(x + 35 * scale, y); t.setheading(0); t.pendown(); t.forward(35 * scale)
