import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math

def knn_visualization():
    # 1. Create a dataset with 2 classes (Apples vs Oranges)
    # Apples: Small & Red (approx weight 150g, color_score 8)
    # Oranges: Large & Orange (approx weight 170g, color_score 4)
    
    np.random.seed(20)
    apples = pd.DataFrame({
        'weight': np.random.normal(140, 10, 15),
        'color_score': np.random.normal(7, 1, 15),
        'label': 'Apple'
    })
    
    oranges = pd.DataFrame({
        'weight': np.random.normal(180, 10, 15),
        'color_score': np.random.normal(3, 1, 15),
        'label': 'Orange'
    })
    
    df = pd.concat([apples, oranges], ignore_index=True)
    
    # 2. New Mystery Fruit
    new_fruit = {'weight': 160, 'color_score': 5.5}
    
    # 3. Calculate Euclidean Distance
    # dist = sqrt((x2-x1)^2 + (y2-y1)^2)
    df['distance'] = np.sqrt(
        (df['weight'] - new_fruit['weight'])**2 + 
        (df['color_score'] - new_fruit['color_score'])**2
    )
    
    # 4. Find K Nearest Neighbors
    K = 5
    neighbors = df.nsmallest(K, 'distance')
    
    # Determine the winning class
    prediction = neighbors['label'].mode()[0]
    
    # 5. Visualization
    plt.figure(figsize=(10, 7))
    
    # Plot known data
    plt.scatter(apples['weight'], apples['color_score'], color='red', s=100, label='Apples', edgecolor='black')
    plt.scatter(oranges['weight'], oranges['color_score'], color='orange', s=100, label='Oranges', edgecolor='black')
    
    # Plot new point
    plt.scatter(new_fruit['weight'], new_fruit['color_score'], color='blue', marker='*', s=300, label='Mystery Fruit')
    
    # Draw connections to neighbors
    for index, row in neighbors.iterrows():
        plt.plot(
            [new_fruit['weight'], row['weight']], 
            [new_fruit['color_score'], row['color_score']], 
            color='gray', linestyle='--', alpha=0.6
        )
    
    # Draw circle radius around K-th neighbor (approximate neighborhood)
    radius = neighbors['distance'].max()
    circle = plt.Circle((new_fruit['weight'], new_fruit['color_score']), radius, color='blue', fill=False, linestyle=':', alpha=0.3)
    plt.gca().add_patch(circle)

    plt.title(f'KNN Classification (K={K}): Prediction = {prediction}', fontsize=15)
    plt.xlabel('Fruit Weight (g)', fontsize=12)
    plt.ylabel('Color Score (1-10)', fontsize=12)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()
