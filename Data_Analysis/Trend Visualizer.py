import pandas as pd
import matplotlib.pyplot as plt

def plot_sales_trends():
    # 1. Embedded Data (Monthly Sales)
    data = {
        'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
        'Revenue': [12000, 14500, 13200, 16000, 19000, 22000, 21500, 24000, 23500, 28000, 32000, 45000],
        'Expenses': [8000, 8500, 8200, 9000, 9500, 10000, 10500, 11000, 11500, 12000, 14000, 18000]
    }
    
    df = pd.DataFrame(data)

    # 2. Create the Plot
    plt.figure(figsize=(10, 6))
    
    # Plot Revenue Line
    plt.plot(df['Month'], df['Revenue'], marker='o', linestyle='-', color='green', label='Revenue', linewidth=2)
    
    # Plot Expenses Line
    plt.plot(df['Month'], df['Expenses'], marker='x', linestyle='--', color='red', label='Expenses', linewidth=2)
    
    # 3. Formatting
    plt.title('Annual Financial Overview', fontsize=16)
    plt.xlabel('Month', fontsize=12)
    plt.ylabel('Amount ($)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend()
    
    # Add data labels for peak revenue
    peak_rev = df['Revenue'].max()
    peak_month = df.loc[df['Revenue'].idxmax(), 'Month']
    plt.annotate(f'Peak: ${peak_rev}', xy=(peak_month, peak_rev), xytext=(peak_month, peak_rev+2000),
                 arrowprops=dict(facecolor='black', shrink=0.05))

    print("Generating plot...")
    plt.show()


