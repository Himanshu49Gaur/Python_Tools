import turtle
import random

def draw_fractal_tree(t, branch_len, angle, level):
    if level > 0:
        t.pensize(level * 1.5) # Thicker branches at lower levels
        if level <= 2:
            t.color("forestgreen") # Leaves/smaller branches
        else:
            t.color("saddlebrown") # Trunk/larger branches

        t.forward(branch_len)
        t.right(angle)
        draw_fractal_tree(t, branch_len * 0.75, angle, level - 1)
        t.left(angle * 2)
        draw_fractal_tree(t, branch_len * 0.75, angle, level - 1)
        t.right(angle)
        t.backward(branch_len) # Go back to the joint
