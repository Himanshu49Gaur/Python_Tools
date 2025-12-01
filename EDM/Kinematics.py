import numpy as np
import matplotlib.pyplot as plt

def kinematics_trinity():
    # Time parameters
    t = np.linspace(0, 10, 1000)
    
    # Physical constants for a damped oscillator
    # Equation: x(t) = A * exp(-gamma*t) * cos(omega*t)
    A = 5.0      # Amplitude
    gamma = 0.5  # Damping coefficient
    omega = 2*np.pi # Angular frequency (1 Hz)
    
    # 1. Displacement (Position)
    pos = A * np.exp(-gamma * t) * np.cos(omega * t)
    
    # 2. Velocity (Derivative of Position)
    # Using numpy gradient for numerical derivative (simulating sensor data processing)
    dt = t[1] - t[0]
    vel = np.gradient(pos, dt)
    
    # 3. Acceleration (Derivative of Velocity)
    acc = np.gradient(vel, dt)
    
    # Plotting: 3 Subplots sharing X-axis
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 10), sharex=True)
    plt.subplots_adjust(hspace=0.1) # Reduce gap between plots
    
    # Plot Position
    ax1.plot(t, pos, color='green', linewidth=2)
    ax1.set_ylabel(r'Position $x(t)$ [m]', fontsize=12, color='green')
    ax1.set_title('Kinematics Trinity: Relationship between x, v, and a', fontsize=14)
    ax1.grid(True)
    ax1.axhline(0, color='black', linewidth=0.5)
    
    # Highlight max displacement envelope
    ax1.plot(t, A * np.exp(-gamma * t), 'g--', alpha=0.3, label='Envelope')
    
    # Plot Velocity
    ax2.plot(t, vel, color='blue', linewidth=2)
    ax2.set_ylabel(r'Velocity $v(t)$ [m/s]', fontsize=12, color='blue')
    ax2.grid(True)
    ax2.axhline(0, color='black', linewidth=0.5)
    # Note: Velocity is zero when Position is max/min
    
    # Plot Acceleration
    ax3.plot(t, acc, color='red', linewidth=2)
    ax3.set_ylabel(r'Accel. $a(t)$ [m/s$^2$]', fontsize=12, color='red')
    ax3.set_xlabel('Time [s]', fontsize=12)
    ax3.grid(True)
    ax3.axhline(0, color='black', linewidth=0.5)
    
    # Add vertical lines to show phase relationship
    # Draw line at first peak of Position
    peak_idx = np.argmax(pos[:100]) # First peak roughly
    peak_t = t[peak_idx]
    
    for ax in [ax1, ax2, ax3]:
        ax.axvline(peak_t, color='gray', linestyle='--', alpha=0.8)

    # Annotations explaining derivative logic
    ax1.text(peak_t + 0.2, pos[peak_idx], 'Max Position', color='green')
    ax2.text(peak_t + 0.2, 0, 'Zero Velocity', color='blue')
    ax3.text(peak_t + 0.2, acc[peak_idx], 'Max Negative Accel', color='red')
    
    print("Graph generated. Notice how Velocity is zero exactly when Position peaks.")
    plt.show()

if __name__ == "__main__":
    kinematics_trinity()
