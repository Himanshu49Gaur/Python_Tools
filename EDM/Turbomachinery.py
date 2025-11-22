import turtle 

def draw_blade_row(t, x, y_start, y_end, width, color):
    t.color(color)
    t.pensize(1)
    count = 4
    step = (y_end - y_start) / count
    
    t.penup()
    t.goto(x, y_start)
    t.setheading(90)
    
    for i in range(count):
        t.penup()
        t.goto(x, y_start + i*step)
        t.pendown()
        # Draw simple airfoil shape
        t.begin_fill()
        t.goto(x + width, y_start + i*step + step/2)
        t.goto(x, y_start + i*step + step)
        t.goto(x, y_start + i*step)
        t.end_fill()
        
        # Mirror bottom
        t.penup()
        t.goto(x, -(y_start + i*step))
        t.pendown()
        t.begin_fill()

def main():
    screen = turtle.Screen()
    screen.setup(width=1000, height=600)
    screen.bgcolor("white")
    screen.title("Propulsion: Turbofan Engine Schematic (Twin Spool)")
    screen.tracer(0)

    t = turtle.Turtle()
    t.hideturtle()

    # --- Centerline ---
    t.penup(); t.goto(-400, 0); t.pendown(); t.color("black"); t.pensize(1)
    t.setheading(0); t.forward(800); t.write(" Centerline", align="left")

    # --- 1. Fan (Low Pressure) ---
    draw_blade_row(t, -350, 50, 180, 40, "darkblue") # Big Fan
    t.penup(); t.goto(-330, 200); t.color("darkblue"); t.write("FAN", font=("Arial", 12, "bold"))

    # --- 2. Low Pressure Compressor (LPC) ---
    draw_blade_row(t, -280, 50, 120, 30, "blue")
    draw_blade_row(t, -250, 50, 115, 30, "blue")

    # --- 3. High Pressure Compressor (HPC) ---
    draw_blade_row(t, -200, 60, 100, 20, "cyan")
    draw_blade_row(t, -180, 60, 95, 20, "cyan")
    draw_blade_row(t, -160, 60, 90, 20, "cyan")

    # --- 4. Combustion Chamber ---
    t.penup(); t.goto(-120, 80); t.pendown(); t.color("red"); t.begin_fill()
    t.goto(-40, 80); t.goto(-50, 60); t.goto(-110, 60); t.goto(-120, 80); t.end_fill()
    # Mirror
    t.penup(); t.goto(-120, -80); t.pendown(); t.begin_fill()
    t.goto(-40, -80); t.goto(-50, -60); t.goto(-110, -60); t.goto(-120, -80); t.end_fill()
    t.penup(); t.goto(-80, 90); t.write("Combustor", align="center")

    # --- 5. High Pressure Turbine (HPT) ---
    draw_blade_row(t, -20, 60, 95, 25, "orange") # Drives HPC

    # --- 6. Low Pressure Turbine (LPT) ---
    draw_blade_row(t, 30, 50, 105, 30, "darkred") 
    draw_blade_row(t, 60, 50, 110, 30, "darkred") # Drives Fan

    # --- Shafts ---
    # N2 Shaft (High Speed - Outer)
    t.penup(); t.goto(-200, 55); t.pendown(); t.color("cyan"); t.pensize(4)
    t.goto(5, 55) # Connects HPC to HPT
    
    # N1 Shaft (Low Speed - Inner)
    t.penup(); t.goto(-350, 45); t.pendown(); t.color("darkblue"); t.pensize(4)
    t.goto(90, 45) # Connects Fan/LPC to LPT

    # --- Casing / Nacelle ---
    t.penup(); t.goto(-360, 190); t.pendown(); t.color("gray"); t.pensize(3)
    t.goto(150, 140) # Bypass duct wall
    t.penup(); t.goto(-360, -190); t.pendown(); t.goto(150, -140)

    # Core Cowling
    t.penup(); t.goto(-300, 130); t.pendown(); t.color("black"); t.pensize(2)
    t.goto(-100, 110); t.goto(120, 60) # Core collapse
    t.penup(); t.goto(-300, -130); t.pendown()
    t.goto(-100, -110); t.goto(120, -60)

    screen.update()
    screen.exitonclick()

if __name__ == "__main__":
    main()

        t.goto(x + width, -(y_start + i*step + step/2))
        t.goto(x, -(y_start + i*step + step))
        t.goto(x, -(y_start + i*step))
        t.end_fill()
