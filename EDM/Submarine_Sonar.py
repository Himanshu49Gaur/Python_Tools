import turtle
import random

def draw_destroyer_outline(t):
    t.penup()
    t.goto(-300, 0)
    t.pendown()
    t.color("black")
    t.pensize(3)
    
    # Hull
    t.begin_fill()
    t.fillcolor("gray")
    t.forward(50) # Stern
    t.setheading(30)
    t.forward(40) # Deck rise
    t.setheading(0)
    t.forward(400) # Deck
    t.setheading(-45)
    t.forward(60) # Bow
    t.setheading(180)
    t.forward(500) # Bottom
    t.setheading(90)
    t.forward(42) # Stern vertical
    t.end_fill()
    
    # Superstructure
    t.penup(); t.goto(-100, 40); t.setheading(0); t.pendown()
    t.begin_fill(); t.forward(150); t.left(90); t.forward(40); t.left(90); t.forward(150); t.left(90); t.forward(40); t.end_fill()
    
    # Funnels
    t.penup(); t.goto(-60, 80); t.setheading(0); t.pendown(); 
    t.begin_fill(); t.left(80); t.forward(40); t.right(80); t.forward(20); t.right(100); t.forward(40); t.end_fill()
    t.penup(); t.goto(-10, 80); t.setheading(0); t.pendown(); 
    t.begin_fill(); t.left(80); t.forward(40); t.right(80); t.forward(20); t.right(100); t.forward(40); t.end_fill()

def draw_dazzle_pattern(t):
    # Overlay random geometric shapes to simulate dazzle
    colors = ["black", "white", "navy", "lightblue"]
    t.pensize(0)
    
    # Limit drawing to roughly the ship area using clip logic (simulated by placing shapes carefully)
    # We will just draw strips over the hull area
    
    for i in range(20):
        t.penup()
        x = random.randint(-280, 150)
        y = random.randint(5, 35)
        t.goto(x, y)
        
        t.color(random.choice(colors))
        t.begin_fill()
        
        type = random.choice(["stripe", "triangle"])
        if type == "stripe":
            angle = random.choice([45, 135, 90])
            t.setheading(angle)
            length = random.randint(30, 80)
            width = random.randint(10, 25)
            t.forward(length); t.right(90); t.forward(width); t.right(90); t.forward(length); t.right(90); t.forward(width)
        else:
            t.circle(random.randint(10, 30), steps=3)
            
        t.end_fill()

import turtle

def draw_sub(t, x, y):
    t.penup()
    t.goto(x, y)
    t.color("black")
    t.fillcolor("darkslategray")
    t.begin_fill()
    
    # Main pressure hull (Ellipse-ish)
    t.setheading(0)
    t.circle(40, 90)
    t.forward(120)
    t.circle(40, 180)
    t.forward(120)
    t.circle(40, 90)
    t.end_fill()
    
    # Sail (Conning Tower)
    t.penup()
    t.goto(x - 20, y + 40)
    t.begin_fill()
    t.setheading(0)
    t.forward(60)
    t.left(90); t.forward(30)
    t.left(90); t.forward(40) # Taper
    t.left(20); t.forward(32)
    t.end_fill()
    
    # Propeller
    t.penup(); t.goto(x - 170, y); t.pensize(4); t.color("gold"); t.pendown()
    t.setheading(120); t.forward(30); t.backward(30)
    t.setheading(240); t.forward(30); t.backward(30)

def draw_sonar_waves(t, start_x, start_y):
    t.color("lime")
    t.pensize(2)
    t.setheading(0)
    
    for i in range(1, 10):
        radius = i * 40
        t.penup()
        t.goto(start_x + 60 + radius, start_y) # Start at right side of circle
        t.setheading(90)
        t.pendown()
        # Draw arc
        t.circle(radius, 45)
        t.penup()
        t.goto(start_x + 60 + radius, start_y)
        t.setheading(90)
        t.pendown()
        t.circle(radius, -45)


def draw_sonar_waves(t, start_x, start_y):
    t.color("lime")
    t.pensize(2)
    t.setheading(0)
    
    for i in range(1, 10):
        radius = i * 40
        t.penup()
        t.goto(start_x + 60 + radius, start_y) # Start at right side of circle
        t.setheading(90)
        t.pendown()
        # Draw arc
        t.circle(radius, 45)
        t.penup()
        t.goto(start_x + 60 + radius, start_y)
        t.setheading(90)
        t.pendown()
        t.circle(radius, -45)

def main():
    screen = turtle.Screen()
    screen.setup(width=900, height=600)
    screen.bgcolor("navy") # Deep ocean
    screen.title("Naval Tech: Active Sonar")
    screen.tracer(0)

    t = turtle.Turtle()
    t.hideturtle()

    # Draw Submarine
    draw_sub(t, -200, 0)
    
    # Draw Target (Sea Mine)
    t.penup(); t.goto(300, 0); t.color("black"); t.fillcolor("red"); t.begin_fill()
    t.circle(20); t.end_fill()
    t.pensize(3); t.goto(300, 20)
    t.pendown(); t.goto(300, 50); t.goto(300, -10)
    t.penup(); t.goto(270, 20); t.pendown(); t.goto(330, 20)
    
    # Emit Sonar
    draw_sonar_waves(t, -200, 0)
    
    # Reflection (Echo) - Dashed lines returning
    t.color("yellow")
    t.pensize(2)
    for i in range(1, 5):
        t.penup()
        t.goto(300 - i*50, 0)
        t.pendown()
        t.circle(10, 360) # Small reflected packets

    t.penup(); t.goto(0, 200); t.color("white"); t.write("ACTIVE SONAR PING", align="center", font=("Courier", 18, "bold"))

    screen.update()
    screen.exitonclick()

if __name__ == "__main__":
    main()
