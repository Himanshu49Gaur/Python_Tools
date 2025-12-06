import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def analyze_correlations():
    # 1. Embedded Data (Marketing Data)
    data = {
        'TV_Ad_Spend': [230, 44, 17, 151, 180, 8, 57, 120, 8, 147],
        'Radio_Ad_Spend': [37, 39, 45, 41, 10, 48, 32, 19, 2, 24],
        'Social_Media_Spend': [69, 45, 69, 58, 58, 75, 23, 11, 1, 55],
        'Sales': [22, 10, 9, 18, 12, 7, 11, 13, 4, 17]
    }
    
    df = pd.DataFrame(data)
    
    # 2. Calculate Correlation Matrix
    # Values range from -1 (perfect negative) to 1 (perfect positive)
    corr_matrix = df.corr()
    
    print("--- Correlation Matrix ---")
    print(corr_matrix)
    print("\n")

    # 3. Visualize with Heatmap
    plt.figure(figsize=(8, 6))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=.5)
    
    plt.title('Correlation Heatmap: Ad Spend vs Sales')
    print("Generating heatmap...")
    plt.show()


