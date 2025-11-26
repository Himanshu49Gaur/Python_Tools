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
