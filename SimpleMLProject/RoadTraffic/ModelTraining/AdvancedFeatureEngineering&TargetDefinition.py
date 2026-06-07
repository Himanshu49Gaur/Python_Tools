import numpy as np

print("Step 2: Advanced Feature Engineering & Defining Target...")

TARGET = 'demand'
test_ids = test_df['Index']

def engineer_features(df):
    """Applies temporal and structural transformations to the dataset."""
    df_engineered = df.copy()
    
    # 1. Temporal Features from 'timestamp' (Format: "H:M")
    df_engineered['hour'] = df_engineered['timestamp'].apply(lambda x: int(str(x).split(':')[0]))
    df_engineered['minute'] = df_engineered['timestamp'].apply(lambda x: int(str(x).split(':')[1]))
    
    # Create a peak hour flag (Assuming 7-10 AM and 4-7 PM are high traffic)
    df_engineered['is_peak_hour'] = df_engineered['hour'].apply(lambda x: 1 if (7 <= x <= 10) or (16 <= x <= 19) else 0)
    
    # Cyclical encoding for hours to preserve the continuous nature of time
    df_engineered['hour_sin'] = np.sin(2 * np.pi * df_engineered['hour'] / 24)
    df_engineered['hour_cos'] = np.cos(2 * np.pi * df_engineered['hour'] / 24)
    
    # 2. Day cycles
    # Assuming 'day' is a sequential integer, extract a synthetic 'day of week'
    df_engineered['day_of_week'] = df_engineered['day'] % 7
    df_engineered['is_weekend'] = df_engineered['day_of_week'].apply(lambda x: 1 if x >= 5 else 0)
    
    return df_engineered

# Apply base engineering to both datasets
train_fe = engineer_features(train_df)
test_fe = engineer_features(test_df)

# 3. Spatial Target Encoding for 'geohash'
# Calculate the mean demand for each geohash ONLY on the training set to prevent leakage
geohash_means = train_fe.groupby('geohash')[TARGET].mean().to_dict()
global_mean = train_fe[TARGET].mean()

# Map the learned means to the datasets
train_fe['geohash_encoded'] = train_fe['geohash'].map(geohash_means)
# For the test set, if a geohash was never seen in training, fill it with the global mean
test_fe['geohash_encoded'] = test_fe['geohash'].map(geohash_means).fillna(global_mean)

# 4. Finalize Feature Selection
# Drop the original unoptimized columns and the Index
cols_to_drop = ['Index', 'timestamp', 'geohash']

X_train = train_fe.drop(columns=cols_to_drop + [TARGET])
y_train = train_fe[TARGET]
X_test = test_fe.drop(columns=cols_to_drop)

print(f"Engineered Training Features (X_train) shape: {X_train.shape}")
print(f"Target (y_train) shape: {y_train.shape}")
print(f"Engineered Testing Features (X_test) shape: {X_test.shape}")
print("\nAdvanced Feature Engineering complete.")
