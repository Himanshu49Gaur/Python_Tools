import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def demonstrate_clt():
    # 1. The Population: A Fair Die (Uniform Distribution)
    # Probabilities are equal for 1, 2, 3, 4, 5, 6
    population_data = np.random.randint(1, 7, size=10000)
    
    # 2. Sampling: Take many samples and calculate their means
    sample_means = []
    n_samples = 1000  # Number of experiments
    sample_size = 50  # Rolls per experiment
    
    for _ in range(n_samples):
        # Roll the die 'sample_size' times
        sample = np.random.choice(population_data, size=sample_size)
        # Record the average
        sample_means.append(np.mean(sample))
    
    df_means = pd.DataFrame(sample_means, columns=['Mean'])

    # 3. Visualization
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Plot 1: The Original Uniform Distribution
    ax1.hist(population_data, bins=6, range=(0.5, 6.5), rwidth=0.8, color='skyblue', edgecolor='black')
    ax1.set_title("Original Distribution (1 Die Roll)", fontsize=12)
    ax1.set_xlabel("Die Value")
    ax1.set_ylabel("Frequency")
    ax1.text(3.5, 1000, "Uniform Shape", ha='center', fontsize=12, fontweight='bold', color='navy')
    
    # Plot 2: The Sampling Distribution (Bell Curve)
    ax2.hist(df_means['Mean'], bins=30, color='salmon', edgecolor='black', alpha=0.8)
    ax2.set_title(f"Distribution of Sample Means (n={sample_size})", fontsize=12)
    ax2.set_xlabel("Average Value")
    ax2.set_ylabel("Frequency")
    
    # Add mean line
    grand_mean = df_means['Mean'].mean()
    ax2.axvline(grand_mean, color='red', linestyle='dashed', linewidth=2)
    ax2.text(grand_mean + 0.05, 50, f"Mean ≈ {grand_mean:.2f}", color='red', fontweight='bold')
    
    plt.suptitle("Central Limit Theorem: From Uniform to Normal Distribution", fontsize=16)
    plt.show()
