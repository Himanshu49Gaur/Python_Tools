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

def main():
    screen = turtle.Screen()
    screen.setup(width=900, height=600)
    screen.bgcolor("lightblue") # Ocean sky
    screen.title("Warship Engineering: Dazzle Camouflage")
    screen.tracer(0)

    t = turtle.Turtle()
    t.hideturtle()
    
    # Draw Ocean
    t.penup(); t.goto(-450, 0); t.pendown(); t.color("teal"); t.begin_fill()
    t.goto(450, 0); t.goto(450, -300); t.goto(-450, -300); t.goto(-450, 0); t.end_fill()

    # Draw Ship
    draw_destroyer_outline(t)
    
    # Apply Dazzle
    # Note: In a real graphics engine we would mask this. 
    # Here we draw patterns on top, but strictly inside visual bounds is hard in Turtle.
    # We will draw "on" the hull coordinates.
    draw_dazzle_pattern(t)
    
    # Re-draw outline to clean up edges
    t.color("black"); t.pensize(3); t.fillcolor(""); 
    draw_destroyer_outline(t)

    t.penup(); t.goto(0, -100); t.color("white"); t.write("Dazzle Camouflage: Breaking the outline", align="center", font=("Stencil", 16, "bold"))

    screen.update()
    screen.exitonclick()

if __name__ == "__main__":
    main()
