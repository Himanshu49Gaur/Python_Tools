import numpy as no
import matplotlib.pyplot as plt

def projectile_simulation():
    # Parameters
    u = 50          # Initial velocity (m/s)
    theta_deg = 45  # Angle of projection (degrees)
    g = 9.81        # Acceleration due to gravity (m/s^2)
    
    theta_rad = np.radians(theta_deg)
    
    # Time of flight
    T = 2 * u * np.sin(theta_rad) / g
    
    # Time array for the smooth curve
    t_fine = np.linspace(0, T, 200)
    
    # Trajectory Equations
    # x = u*cos(theta)*t
    # y = u*sin(theta)*t - 0.5*g*t^2
    x_fine = u * np.cos(theta_rad) * t_fine
    y_fine = u * np.sin(theta_rad) * t_fine - 0.5 * g * t_fine**2
    
    # Specific time points for vectors (to avoid clutter)
    t_vec = np.linspace(0, T, 10)
    x_vec = u * np.cos(theta_rad) * t_vec
    y_vec = u * np.sin(theta_rad) * t_vec - 0.5 * g * t_vec**2
    
    # Velocity components at vector points
    # vx is constant, vy changes: vy = uy - gt
    vx = np.full_like(t_vec, u * np.cos(theta_rad))
    vy = u * np.sin(theta_rad) - g * t_vec

    # Plotting
    plt.figure(figsize=(12, 7))
    plt.style.use('seaborn-v0_8-darkgrid')
    
    # Plot Trajectory Path
    plt.plot(x_fine, y_fine, 'k--', linewidth=1.5, label='Trajectory Path')
    
    # Plot Vectors
    quiver_scale = 20 # Adjustment for vector visual length
    
    # Total Velocity Vectors (Red)
    plt.quiver(x_vec, y_vec, vx, vy, color='red', angles='xy', scale_units='xy', scale=3, width=0.005, label=r'Velocity $\vec{v}$')
    
    # Horizontal Components (Blue - Dashed)
    plt.quiver(x_vec, y_vec, vx, np.zeros_like(vy), color='blue', angles='xy', scale_units='xy', scale=3, width=0.003, alpha=0.6, label=r'$v_x$ (Constant)')
    
    # Vertical Components (Green - Dashed)
    plt.quiver(x_vec, y_vec, np.zeros_like(vx), vy, color='green', angles='xy', scale_units='xy', scale=3, width=0.003, alpha=0.6, label=r'$v_y$ (Changing)')

    # Labels and Title
    plt.title(f'Projectile Motion Vector Analysis (Initial Velocity: {u}m/s, Angle: {theta_deg}°)', fontsize=14)
    plt.xlabel('Distance (m)', fontsize=12)
    plt.ylabel('Height (m)', fontsize=12)
    plt.legend(loc='upper right')
    plt.grid(True)
    plt.axis('equal') # Ensure aspect ratio is 1:1 so vectors aren't distorted
    plt.ylim(bottom=0)
    
    # Equation Annotation
    equation_text = r"$y = x\tan(\theta) - \frac{gx^2}{2u^2\cos^2(\theta)}$"
    plt.text(x_fine.max()*0.6, y_fine.max()*0.9, equation_text, fontsize=14, bbox=dict(facecolor='white', alpha=0.8))

    plt.show()

if __name__ == "__main__":
    projectile_simulation()
