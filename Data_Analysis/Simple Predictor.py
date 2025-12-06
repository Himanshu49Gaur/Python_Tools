import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

def predict_house_prices():
    # 1. Embedded Data (Square Footage vs Price)
    # X needs to be 2D array for sklearn
    data = {
        'Size_sqft': [1500, 1600, 1700, 1850, 2000, 2200, 2400, 2550],
        'Price_usd': [300000, 320000, 340000, 365000, 400000, 435000, 480000, 510000]
    }
    
    df = pd.DataFrame(data)
    X = df[['Size_sqft']] # Features
    y = df['Price_usd']   # Target
    
    # 2. Create and Train Model
    model = LinearRegression()
    model.fit(X, y)
    
    print(f"Model Trained. Slope (Coefficient): {model.coef_[0]:.2f}")
    
    # 3. Make a Prediction
    new_house_size = [[1900]] # Predicting price for a 1900 sqft house
    predicted_price = model.predict(new_house_size)
    
    print(f"Predicted price for a 1,900 sqft house: ${predicted_price[0]:,.2f}")
    
    # 4. Visualize the Regression Line
    plt.scatter(X, y, color='blue', label='Actual Data')
    plt.plot(X, model.predict(X), color='red', label='Regression Line')
    
    # Plot the prediction point
    plt.scatter(new_house_size, predicted_price, color='green', s=100, zorder=5, label='Prediction')
    
    plt.xlabel('Size (sqft)')
    plt.ylabel('Price (USD)')
    plt.title('House Price Prediction Model')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()
