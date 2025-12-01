import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def time_series_analysis():
    # 1. Generate Synthetic Time Series Data (Random Walk + Trend)
    np.random.seed(42)
    days = 200
    date_range = pd.date_range(start='2023-01-01', periods=days)
    
    # Base trend (linear increase)
    trend = np.linspace(0, 20, days) 
    # Seasonality (sine wave)
    seasonality = 5 * np.sin(np.linspace(0, 6*np.pi, days))
    # Noise (random jitters)
    noise = np.random.normal(0, 3, days)
    
    raw_data = 50 + trend + seasonality + noise
    
    df = pd.DataFrame({'Date': date_range, 'Value': raw_data})
    df.set_index('Date', inplace=True)
    
    # 2. Apply Smoothing Algorithms (Pandas Rolling Window)
    # Simple Moving Average (SMA) - 7 Day
    df['SMA_7'] = df['Value'].rolling(window=7).mean()
    
    # Simple Moving Average (SMA) - 30 Day
    df['SMA_30'] = df['Value'].rolling(window=30).mean()
    
    # Exponential Weighted Moving Average (EWMA) - more weight to recent data
    df['EWMA_30'] = df['Value'].ewm(span=30, adjust=False).mean()

    # 3. Visualization
    plt.figure(figsize=(12, 6))
    
    # Plot Raw noisy data
    plt.plot(df.index, df['Value'], color='lightgray', linewidth=2, label='Raw Noisy Data')
    
    # Plot Short-term Trend
    plt.plot(df.index, df['SMA_7'], color='blue', linewidth=1.5, alpha=0.8, label='7-Day SMA')
    
    # Plot Long-term Trend
    plt.plot(df.index, df['SMA_30'], color='red', linewidth=2, label='30-Day SMA')
    
    # Plot Exponential Trend
    plt.plot(df.index, df['EWMA_30'], color='green', linestyle='--', linewidth=1.5, label='30-Day EWMA')

    plt.title('Time Series Analysis: Extracting Trends from Noise', fontsize=14)
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Value', fontsize=12)
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Highlight the lag effect
    plt.text(df.index[100], 45, "Note how SMA_30 lags behind\nthe sudden changes!", fontsize=10, bbox=dict(facecolor='white', alpha=0.8))
    
    plt.show()
