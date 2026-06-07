print("Step 3: Handling Missing Values (Updated)...")

# 1. Handle Numerical Missing Values (Temperature)
temp_median = X_train['Temperature'].median()

X_train['Temperature'] = X_train['Temperature'].fillna(temp_median)
X_test['Temperature'] = X_test['Temperature'].fillna(temp_median)

# 2. Handle Categorical Missing Values (RoadType, Weather)
cat_cols_with_na = ['RoadType', 'Weather']

for col in cat_cols_with_na:
    X_train[col] = X_train[col].fillna('Unknown')
    X_test[col] = X_test[col].fillna('Unknown')

print(f"Total missing values in X_train: {X_train.isnull().sum().sum()}")
print(f"Total missing values in X_test: {X_test.isnull().sum().sum()}")
