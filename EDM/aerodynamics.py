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
