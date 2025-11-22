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

def draw_fpm(t):
    # Flight Path Marker (The little airplane symbol)
    t.penup(); t.goto(0, 0); t.pendown()
    t.color("lime") # Changed from 'brightgreen' to 'lime'
    t.pensize(3)
    t.circle(10)
    t.penup(); t.goto(-20, 0); t.pendown(); t.goto(-10, 0) # Left wing
    t.penup(); t.goto(10, 0); t.pendown(); t.goto(20, 0) # Right wing
    t.penup(); t.goto(0, 10); t.pendown(); t.goto(0, 20) # Top tail

def main():
    screen = turtle.Screen()
    screen.setup(width=800, height=600)
    screen.bgcolor("black") # Night mode
    screen.title("Avionics: Heads-Up Display (HUD)")
    screen.tracer(0)
    
    # Register colors if needed or use standard
    try:
        screen.colormode(255)
    except:
        pass

    t = turtle.Turtle()
    t.hideturtle()
    # using RGB tuple for the main color setting, or standard names
    t.color(0, 255, 0) 

    # 1. Horizon Line
    t.penup(); t.goto(-300, 0); t.pendown()
    t.pensize(2)
    t.goto(300, 0)
    t.penup(); t.goto(310, -5); t.write("00", font=("Consolas", 12, "bold"))

    # 2. Pitch Ladder (Positive)
    draw_pitch_line(t, 50, 150, "05")
    draw_pitch_line(t, 100, 150, "10")
    draw_pitch_line(t, 150, 150, "15")

    # 3. Pitch Ladder (Negative - dashed usually, but solid here for simplicity)
    draw_pitch_line(t, -50, 150, "-05")
    draw_pitch_line(t, -100, 150, "-10")

    # 4. Flight Path Marker (Velocity Vector)
    # Placed slightly above horizon implying a climb
    t.penup(); t.goto(0, 20); 
    # Redraw FPM manually at 0, 20
    t.color("lime")
    t.goto(0, 10); t.pendown(); t.circle(10)
    t.penup(); t.goto(-20, 20); t.pendown(); t.goto(-10, 20)
    t.penup(); t.goto(10, 20); t.pendown(); t.goto(20, 20)
    t.penup(); t.goto(0, 30); t.pendown(); t.goto(0, 40)

    # 5. Airspeed and Altitude Tapes
    # Airspeed (Left)
    t.penup(); t.goto(-250, 0); t.pendown()
    t.color("lime")
    t.goto(-250, 150); t.goto(-320, 150); t.goto(-320, -150); t.goto(-250, -150); t.goto(-250, 0)
    t.penup(); t.goto(-300, -10); t.write("320", font=("Consolas", 16, "bold")) # Current Speed
    t.goto(-240, 160); t.write("KNOTS", font=("Consolas", 10, "normal"))

    # Altitude (Right)
    t.penup(); t.goto(250, 0); t.pendown()
    t.goto(250, 150); t.goto(340, 150); t.goto(340, -150); t.goto(250, -150); t.goto(250, 0)
    t.penup(); t.goto(260, -10); t.write("14,500", font=("Consolas", 16, "bold")) # Current Alt
    t.goto(260, 160); t.write("FEET", font=("Consolas", 10, "normal"))

    # 6. Heading Tape (Top)
    t.penup(); t.goto(-150, 250); t.pendown()
    t.goto(150, 250)
    for i in range(-2, 3):
        x = i * 50
        t.penup(); t.goto(x, 250); t.pendown(); t.goto(x, 260)
        t.penup(); t.goto(x - 10, 265); t.write(f"{18+i}0", font=("Consolas", 10, "bold"))
    
    # Caret
    t.penup(); t.goto(0, 240); t.pendown(); t.goto(-10, 230); t.goto(10, 230); t.goto(0, 240)

    screen.update()
    screen.exitonclick()

if __name__ == "__main__":
    main()
