import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def simple_linear_regression():
    # 1. Create a synthetic dataset (Experience vs Salary)
    np.random.seed(42)
    n_samples = 50
    X = np.random.rand(n_samples) * 10 # Years of experience (0 to 10)
    # y = 30k + 8k * X + noise
    true_intercept = 30000
    true_slope = 8000
    noise = np.random.randn(n_samples) * 5000 # Random variation
    y = true_intercept + true_slope * X + noise

    df = pd.DataFrame({'Experience': X, 'Salary': y})

    # 2. The Algorithm: Ordinary Least Squares (OLS)
    # Formula: m = sum((x - x_mean)(y - y_mean)) / sum((x - x_mean)^2)
    x_mean = df['Experience'].mean()
    y_mean = df['Salary'].mean()

    numerator = np.sum((df['Experience'] - x_mean) * (df['Salary'] - y_mean))
    denominator = np.sum((df['Experience'] - x_mean) ** 2)

    m = numerator / denominator
    b = y_mean - (m * x_mean)

    # 3. Make Predictions
    df['Predicted_Salary'] = m * df['Experience'] + b

    # 4. Visualization
    plt.figure(figsize=(10, 6))
    
    # Scatter plot of actual data
    plt.scatter(df['Experience'], df['Salary'], color='blue', alpha=0.6, label='Actual Data')
    
    # Line of best fit
    plt.plot(df['Experience'], df['Predicted_Salary'], color='red', linewidth=2, label=f'Best Fit Line: y = {m:.0f}x + {b:.0f}')
    
    # Show residuals (errors) for a few points
    for i in range(0, n_samples, 5): # Draw lines for every 5th point
        x_pt = df['Experience'].iloc[i]
        y_real = df['Salary'].iloc[i]
        y_pred = df['Predicted_Salary'].iloc[i]
        plt.vlines(x_pt, y_real, y_pred, colors='gray', linestyles='--', alpha=0.5)

    plt.title('Linear Regression from Scratch: Experience vs Salary', fontsize=14)
    plt.xlabel('Years of Experience', fontsize=12)
    plt.ylabel('Salary ($)', fontsize=12)
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    print(f"Model Learned:\nSlope (m): {m:.2f}\nIntercept (b): {b:.2f}")
    plt.show()

if __name__ == "__main__":
    simple_linear_regression()
