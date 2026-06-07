from sklearn.preprocessing import StandardScaler, LabelEncoder

print("Step 4: Standardizing and Encoding Features (Updated)...")

# ---------------------------------------------------------
# 1. Standardize Numerical Features
# ---------------------------------------------------------
# We include our new continuous engineered features here
num_cols = ['day', 'NumberofLanes', 'Temperature', 'hour', 'minute', 'day_of_week', 'geohash_encoded']

scaler = StandardScaler()

# Fit on training, transform both
X_train[num_cols] = scaler.fit_transform(X_train[num_cols])
X_test[num_cols] = scaler.transform(X_test[num_cols])

# ---------------------------------------------------------
# 2. Encode Categorical Features
# ---------------------------------------------------------
# geohash and timestamp have been removed from this list!
cat_cols = ['RoadType', 'LargeVehicles', 'Landmarks', 'Weather']

for col in cat_cols:
    le = LabelEncoder()
    
    # Fit on combined data to ensure all unique categories are captured
    combined_data = list(X_train[col]) + list(X_test[col])
    le.fit(combined_data)
    
    X_train[col] = le.transform(X_train[col])
    X_test[col] = le.transform(X_test[col])

print("Feature standardization and categorical encoding complete!")
print("\nSample of processed training features (X_train):")
display(X_train.head(3))
