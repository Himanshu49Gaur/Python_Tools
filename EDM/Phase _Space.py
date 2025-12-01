import numpy as np
import matplotlib.pyplot as plt

def phase_space_portrait():
    # Parameters for Simple Harmonic Motion
    k = 5.0  # Spring constant
    m = 1.0  # Mass
    omega = np.sqrt(k / m) # Angular frequency
    
    # Create distinct Energy levels (Initial Displacements)
    initial_displacements = [1.0, 2.0, 3.0, 4.0] # Different Amplitudes
    
    t = np.linspace(0, 10, 500)
    
    fig, ax = plt.subplots(figsize=(8, 8))
    
    # Color map for different energies
    colors = plt.cm.viridis(np.linspace(0, 1, len(initial_displacements)))
    
    for i, A in enumerate(initial_displacements):
        # Equations of motion
        x = A * np.cos(omega * t)          # Position
        v = -A * omega * np.sin(omega * t) # Velocity
        
        # Calculate Total Energy for this orbit
        # E = 0.5*k*x^2 + 0.5*m*v^2
        E = 0.5 * k * A**2
        
        # Plot the Phase Space Orbit (v vs x)
        ax.plot(x, v, color=colors[i], linewidth=2, label=f'Energy: {E:.1f} J')
        
        # Add velocity direction arrows on the path
        # Arrow logic: at x=0, v is max negative or positive
        ax.arrow(0, A*omega, 0.1, 0, head_width=0.2, head_length=0.2, fc=colors[i], ec=colors[i])
        ax.arrow(0, -A*omega, -0.1, 0, head_width=0.2, head_length=0.2, fc=colors[i], ec=colors[i])

    # Styling
    ax.set_title('Phase Space Portrait: Simple Harmonic Motion', fontsize=14)
    ax.set_xlabel('Position $x$ (m)', fontsize=12)
    ax.set_ylabel('Velocity $v$ (m/s)', fontsize=12)
    
    # Axes lines
    ax.axhline(0, color='black', linewidth=1)
    ax.axvline(0, color='black', linewidth=1)
    
    # Grid and Legend
    ax.grid(True, linestyle='--')
    ax.legend(loc='upper right', title="Total Energy Levels")
    
    # Annotation
    text_expl = (
        "Circular/Elliptical paths indicate\n"
        "Conservation of Energy.\n"
        r"$E_{total} = \frac{1}{2}kx^2 + \frac{1}{2}mv^2 = const$"
    )
    ax.text(-3.5, -3.5, text_expl, fontsize=10, bbox=dict(facecolor='white', alpha=0.9))

    plt.axis('equal') # Essential for Phase Space to look correct
    plt.show()
