from sklearn.model_selection import train_test_split

print("Creating Local Validation Split...")

# We will use 80% of the training data to train the models 
# and hold back 20% to evaluate our R-squared score locally.
X_trn, X_val, y_trn, y_val = train_test_split(
    X_train, 
    y_train, 
    test_size=0.20, 
    random_state=42 # Setting a random state ensures reproducibility
)

print(f"Local Training Data shape: {X_trn.shape}")
print(f"Local Validation Data shape: {X_val.shape}")
print(f"Kaggle Test Data (for final submission) shape: {X_test.shape}")
