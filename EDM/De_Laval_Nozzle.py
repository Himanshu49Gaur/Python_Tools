import turtle 
import math 

def draw_nozzle_curve(t, start_x, start_y, length, throat_y, exit_y, mirror=False):
    t.penup()
    t.goto(start_x, start_y)
    t.pendown()
    t.color("white")
    t.pensize(3)
    
    steps = 50
    dx = length / steps
    
    # Using a cosine function to approximate the bell nozzle shape
    for i in range(steps + 1):
        x = start_x + i * dx
        progress = i / steps
        
        # Interpolate radius: Start -> Throat -> Exit
        # We use a composite curve logic here
        if progress < 0.3: # Converging section
            local_progress = progress / 0.3
            # Curve down to throat
            y = start_y - (start_y - throat_y) * math.sin(local_progress * math.pi / 2)
        else: # Diverging section
            local_progress = (progress - 0.3) / 0.7
            # Curve out to exit
            y = throat_y + (exit_y - throat_y) * (1 - math.cos(local_progress * math.pi / 2))
            
        if mirror:
            t.goto(x, -y)
        else:
            t.goto(x, y)
