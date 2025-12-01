import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def kmeans_from_scratch():
    # 1. Generate random data blobs
    np.random.seed(10)
    
    # Cluster 1
    c1 = np.random.normal(loc=[2, 2], scale=0.8, size=(50, 2))
    # Cluster 2
    c2 = np.random.normal(loc=[8, 8], scale=0.8, size=(50, 2))
    # Cluster 3
    c3 = np.random.normal(loc=[8, 2], scale=0.8, size=(50, 2))
    
    data = np.vstack([c1, c2, c3])
    df = pd.DataFrame(data, columns=['x', 'y'])

    # 2. Initialization: Pick K random points as centroids
    k = 3
    centroids = df.sample(n=k).values
    
    # 3. The Algorithm Loop (Simplified for demonstration)
    # We will run just one iteration to show the logic, or loop a few times
    for iteration in range(5):
        # Step A: Assign points to nearest centroid
        distances = []
        for i in range(k):
            # Euclidean distance: sqrt((x2-x1)^2 + (y2-y1)^2)
            dist = np.sqrt(((df[['x', 'y']].values - centroids[i]) ** 2).sum(axis=1))
            distances.append(dist)
        
        # Determine closest cluster for each point
        df['cluster'] = np.argmin(distances, axis=0)
        
        # Step B: Update centroids to be the mean of points in the cluster
        new_centroids = []
        for i in range(k):
            cluster_points = df[df['cluster'] == i][['x', 'y']]
            if len(cluster_points) > 0:
                new_centroids.append(cluster_points.mean().values)
            else:
                new_centroids.append(centroids[i]) # Keep old if empty
        centroids = np.array(new_centroids)

    # 4. Visualization
    plt.figure(figsize=(10, 6))
    
    colors = ['#FF9999', '#99FF99', '#9999FF']
    
    for i in range(k):
        cluster_data = df[df['cluster'] == i]
        plt.scatter(cluster_data['x'], cluster_data['y'], c=colors[i], s=50, label=f'Cluster {i+1}')
        
        # Plot Centroids
        plt.scatter(centroids[i][0], centroids[i][1], c='black', marker='X', s=200, edgecolor='white', label=f'Centroid {i+1}')

    plt.title(f'K-Means Clustering: Grouping Data into {k} Clusters', fontsize=14)
    plt.xlabel('Feature 1', fontsize=12)
    plt.ylabel('Feature 2', fontsize=12)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()
