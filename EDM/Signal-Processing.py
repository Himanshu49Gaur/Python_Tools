import turtle
import math

def main():
    screen = turtle.Screen()
    screen.setup(width=1000, height=600)
    screen.bgcolor("black")
    screen.title("Signal Processing: Amplitude Modulation (AM)")
    screen.tracer(0)

    t = turtle.Turtle()
    t.hideturtle()
    t.color("green")
    t.pensize(2)

    # Draw Axes
    t.color("white")
    t.penup()
    t.goto(-450, 0)
    t.pendown()
    t.goto(450, 0) # X Axis
    t.penup()
    t.goto(-400, -250)
    t.pendown()
    t.goto(-400, 250) # Y Axis

    # Parameters
    carrier_freq = 0.5
    msg_freq = 0.05
    amplitude = 100
    
    t.color("cyan")
    t.penup()
    
    # Draw the modulated wave
    # Formula: y = (1 + m * sin(msg_freq * x)) * sin(carrier_freq * x)
    start_x = -400
    end_x = 400
    
    t.goto(start_x, 0)
    t.pendown()
    
    for x in range(start_x, end_x):
        # Message signal (Envelope)
        envelope = 1 + 0.5 * math.sin(msg_freq * (x - start_x))
        # Carrier wave
        carrier = math.sin(carrier_freq * (x - start_x))
        
        y = amplitude * envelope * carrier
        t.goto(x, y)

    # Draw the Envelope (Ghost line)
    t.color("red")
    t.pensize(1)
    t.penup()
    for x in range(start_x, end_x):
        envelope = 1 + 0.5 * math.sin(msg_freq * (x - start_x))
        y = amplitude * envelope
        if x == start_x:
            t.goto(x, y)
            t.pendown()
        else:
            t.goto(x, y)

    # Draw labels
    t.penup()
    t.goto(-380, 220)
    t.color("red")
    t.write("Message Envelope", font=("Courier", 12, "bold"))
    t.goto(-380, 190)
    t.color("cyan")
    t.write("Modulated Carrier", font=("Courier", 12, "bold"))

    screen.update()
    screen.exitonclick()

if __name__ == "__main__":
    main()
