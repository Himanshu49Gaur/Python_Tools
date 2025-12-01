import numpy as np
import matplotlib.pyplot as plt

def terminal_velocity_simulation():
    # Parameters
    m = 70      # Mass of skydiver (kg)
    g = 9.81    # Gravity (m/s^2)
    rho = 1.225 # Air density (kg/m^3)
    Cd = 1.0    # Drag coefficient
    A = 0.5     # Cross-sectional area (m^2)
    
    # Calculate Terminal Velocity
    # mg = 0.5 * rho * v^2 * Cd * A
    v_terminal = np.sqrt((2 * m * g) / (rho * A * Cd))
    
    # Time array
    t = np.linspace(0, 15, 200)
    
    # 1. Velocity in Vacuum (No Drag): v = gt
    v_vacuum = g * t
    
    # 2. Velocity with Drag (Analytical Solution)
    # v(t) = vt * tanh( (g*t) / vt )
    v_drag = v_terminal * np.tanh((g * t) / v_terminal)
    
    # Plotting
    plt.figure(figsize=(10, 6))
    plt.style.use('bmh')
    
    # Plot Vacuum Line
    plt.plot(t, v_vacuum, 'k--', label='Vacuum (No Drag) $v=gt$', alpha=0.5)
    
    # Plot Drag Curve
    plt.plot(t, v_drag, 'r-', linewidth=3, label='With Air Resistance')
    
    # Plot Terminal Velocity Asymptote
    plt.axhline(v_terminal, color='blue', linestyle=':', linewidth=2, label=f'Terminal Velocity ({v_terminal:.1f} m/s)')
    
    # Fill area showing "Drag Effect" (Difference in speed)
    plt.fill_between(t, v_drag, v_vacuum, where=(t < 6), color='gray', alpha=0.1)
    plt.text(2, 40, 'Effect of Drag Force', rotation=45, color='gray')

    # Annotations
    plt.title('Terminal Velocity: The Balance of Gravity and Drag', fontsize=14)
    plt.xlabel('Time (s)', fontsize=12)
    plt.ylabel('Velocity (m/s)', fontsize=12)
    plt.ylim(0, v_terminal * 1.5)
    plt.xlim(0, 15)
    
    # Add Equation Box
    eq_text = (
        r"$v_{term} = \sqrt{\frac{2mg}{\rho A C_d}}$" + "\n" +
        r"$v(t) = v_{term} \tanh\left(\frac{gt}{v_{term}}\right)$"
    )
    plt.text(8, 20, eq_text, fontsize=16, bbox=dict(facecolor='white', edgecolor='red', pad=10))

    plt.legend()
    plt.grid(True)
    plt.show()
