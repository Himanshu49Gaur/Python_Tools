import pandas as pd
import os

# Define the base path for your Kaggle dataset
# Note: Kaggle converts dataset names to lowercase in the file path
BASE_PATH = '/kaggle/input/datasets/himanshugaur49/thenewdataset'

print("Loading datasets...")

# 1. Load the dataset
train_df = pd.read_csv(os.path.join(BASE_PATH, 'train.csv'))
test_df = pd.read_csv(os.path.join(BASE_PATH, 'test.csv'))

# Load the sample submission file to ensure our final output matches the required format
sample_sub = pd.read_csv(os.path.join(BASE_PATH, 'sample_submission.csv'))

# Verify the data has been loaded correctly by checking their shapes
print(f"Train dataset shape: {train_df.shape}")
print(f"Test dataset shape: {test_df.shape}")
print(f"Sample submission shape: {sample_sub.shape}")
print("\nDatasets loaded successfully!")
