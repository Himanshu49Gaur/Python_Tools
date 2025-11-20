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

def draw_connection_dot(t, x, y):
    t.penup(); t.goto(x, y-3); t.pendown(); t.begin_fill(); t.circle(3); t.end_fill()

def main():
    screen = turtle.Screen()
    screen.setup(width=800, height=600)
    screen.title("Digital Logic: Half Adder Schematic (Corrected)")
    screen.tracer(0) 

    t = turtle.Turtle()
    t.hideturtle()
    t.speed(0)

    # --- Layout Configuration ---
    input_x = -200
    gate_x = 50       # Gates are aligned horizontally
    xor_y = 60        # XOR gate height
    and_y = -60       # AND gate height
    
    # --- Draw Inputs Labels ---
    t.penup(); t.goto(input_x - 20, xor_y + 40); t.write("A", font=("Arial", 16, "bold"))
    t.penup(); t.goto(input_x - 20, and_y - 40); t.write("B", font=("Arial", 16, "bold"))

    # --- Wire A (Top Signal) ---
    # Logic: From Source A -> Split Point -> To XOR -> To AND
    t.pensize(2)
    t.penup(); t.goto(input_x, xor_y + 10); t.pendown() # Start at A height
    t.goto(-50, xor_y + 10) # Go forward to split line
    
    # Split to XOR (Top input)
    t.goto(gate_x - 20, xor_y + 10) 
    
    # Split to AND (Top input)
    t.penup(); t.goto(-50, xor_y + 10); t.pendown()
    t.goto(-50, and_y + 10) # Drop down
    t.goto(gate_x, and_y + 10) # Connect to AND
    
    draw_connection_dot(t, -50, xor_y + 10) # Draw dot at intersection

    # --- Wire B (Bottom Signal) ---
    # Logic: From Source B -> Split Point -> To XOR -> To AND
    t.penup(); t.goto(input_x, and_y - 10); t.pendown() # Start at B height
    t.goto(-70, and_y - 10) # Go forward to split line
    
    # Split to AND (Bottom input)
    t.goto(gate_x, and_y - 10)

    # Split to XOR (Bottom input)
    t.penup(); t.goto(-70, and_y - 10); t.pendown()
    t.goto(-70, xor_y - 10) # Go up
    t.goto(gate_x - 20, xor_y - 10) # Connect to XOR
    
    draw_connection_dot(t, -70, and_y - 10) # Draw dot at intersection

    # --- Draw Gates ---
    # Note: We pass scale=1.5 to make them clearly visible
    draw_xor_gate(t, gate_x, xor_y, 1.5)
    draw_and_gate(t, gate_x, and_y, 1.5)

    # --- Draw Outputs ---
    # XOR Output (Sum)
    t.penup(); t.goto(gate_x + 70, xor_y); t.pendown(); t.forward(50)
    t.penup(); t.goto(gate_x + 130, xor_y - 5); t.write("SUM", font=("Arial", 12, "bold"))

    # AND Output (Carry)
    t.penup(); t.goto(gate_x + 75, and_y); t.pendown(); t.forward(45)
    t.penup(); t.goto(gate_x + 130, and_y - 5); t.write("CARRY", font=("Arial", 12, "bold"))

    screen.update()
    screen.exitonclick()

if __name__ == "__main__":
    main()
