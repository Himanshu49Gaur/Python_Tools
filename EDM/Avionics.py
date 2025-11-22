import turtle

def draw_pitch_line(t, y, width, label):
    t.penup()
    t.goto(-width/2, y)
    t.pendown()
    t.color("lime") # Changed from 'brightgreen' to 'lime'
    t.pensize(2)
    
    # Left tab
    t.setheading(90); t.forward(10); t.setheading(0); t.forward(width/3)
    
    # Gap for FPM
    t.penup(); t.forward(width/3); t.pendown()
    
    # Right tab
    t.forward(width/3); t.setheading(90); t.forward(10)
    
    # Label
    t.penup()
    t.goto(-width/2 - 25, y + 2)
    t.write(label, font=("Consolas", 10, "bold"))
    t.goto(width/2 + 5, y + 2)
    t.write(label, font=("Consolas", 10, "bold"))
