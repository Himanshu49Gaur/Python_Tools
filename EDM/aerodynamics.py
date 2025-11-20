import turtle
import math

def draw_airfoil(t, x, y, chord, camber):
    t.penup()
    t.goto(x + chord, y) # Trailing edge
    t.pendown()
    t.color("black", "gray")
    t.begin_fill()
    
    # Approximate a NACA airfoil shape using a parametric loop
    # We trace from trailing edge (1,0) forward to leading edge (0,0) and back
    steps = 100
    for i in range(steps * 2 + 1):
        beta = (i / (steps * 2)) * (2 * math.pi)
        # X coordinate goes 1 -> 0 -> 1
        px = 0.5 * (1 + math.cos(beta))
        
        # Y coordinate (thickness distribution)
        # Standard NACA 4-digit thickness formula approximation
        thickness = 0.12 # 12% thickness
        yt = 5 * thickness * (0.2969 * math.sqrt(px) - 0.1260 * px - 0.3516 * px**2 + 0.2843 * px**3 - 0.1015 * px**4)
        
        if i <= steps:
            py = yt # Upper surface
        else:
            py = -yt # Lower surface
            
        t.goto(x + px * chord, y + py * chord)
    
    t.end_fill()

def draw_streamline(t, start_x, start_y, length, airfoil_x, airfoil_y, chord):
    t.penup()
    t.goto(start_x, start_y)
    t.pendown()
    t.color("blue")
    t.pensize(1)
    
    step = 5
    current_x = start_x
    current_y = start_y
    
    while current_x < start_x + length:
        # Simple potential flow simulation logic:
        # If close to the airfoil x-range, deflect y based on proximity to y=0
        dist_x = abs((current_x - (airfoil_x + chord/3))) # Focus deflection near leading edge
        deflection = 0
        
        if abs(current_x - (airfoil_x + chord/2)) < chord:
             # Push streamlines away from the center line
             factor = 1500 / (dist_x + 10)
             if current_y > airfoil_y:
                 deflection = math.exp(-dist_x/100) * 2
             else:
                 deflection = -math.exp(-dist_x/100) * 2
                 
        t.goto(current_x, current_y + deflection)
        current_x += step
        # current_y += deflection # Accumulate deflection? No, just visual bending
