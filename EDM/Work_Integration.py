import numpy as np
import matplotlib.pyplot as plt

def work_done_simulation():
    # Define a variable force function F(x)
    # Example: A non-linear spring + a damping factor
    # F(x) = kx + x^2 - constant
    def force_func(x):
        return 10 + 2*x + 0.5*x**2 + 5*np.sin(x)

    # Range of displacement (meters)
    x_start = 0
    x_end = 10
    
    # Continuous data for the curve
    x = np.linspace(x_start, x_end, 500)
    y = force_func(x)
    
    # Plotting
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # 1. Plot the Force Curve
    ax.plot(x, y, color='darkblue', linewidth=2.5, label=r'Force $F(x)$')
    
    # 2. Shade the Area (Work Done)
    ax.fill_between(x, y, 0, color='skyblue', alpha=0.4, label='Work Done (Area)')
    
    # 3. Add Riemann Sum Bars (Visualizing the Integral concept)
    num_bars = 10
    x_bars = np.linspace(x_start, x_end, num_bars, endpoint=False)
    bar_width = (x_end - x_start) / num_bars
    
    # Use midpoint for bar height to look cleaner
    y_bars = force_func(x_bars + bar_width/2) 
    
    ax.bar(x_bars + bar_width/2, y_bars, width=bar_width, 
           edgecolor='navy', color='none', linestyle='--', alpha=0.5, label='Riemann Sum $\Sigma F \Delta x$')

    # Calculate actual work (numerical integration)
    work_total = np.trapz(y, x)
    
    # Annotations
    ax.set_title(r'Work Done by Variable Force: $W = \int_{x_1}^{x_2} F(x) dx$', fontsize=15)
    ax.set_xlabel('Displacement $x$ (meters)', fontsize=12)
    ax.set_ylabel('Force $F$ (Newtons)', fontsize=12)
    
    # Place text showing the calculated value
    ax.text(2, np.max(y)*0.8, f"Total Work ≈ {work_total:.2f} Joules", 
            fontsize=12, bbox=dict(facecolor='yellow', alpha=0.2))
    
    # Physics Arrow annotation
    ax.annotate('Force varies with position', xy=(5, force_func(5)), xytext=(2, force_func(5)+20),
                arrowprops=dict(facecolor='black', shrink=0.05))

    ax.legend(fontsize=10)
    ax.grid(True, linestyle=':')
    plt.show()
