import pandas as pd

print("Step 11: Preparing Final AutoGluon Submission File...")

# 1. Create the submission DataFrame
# We map the saved test_ids to the final AutoGluon predictions
submission_df = pd.DataFrame({
    'Index': test_ids,
    'demand': test_predictions_ag
})

# 2. Sanity Checks
# Verifying dimensions and column names match the sample_submission.csv format strictly
print("Performing Sanity Checks...")
expected_shape = (41778, 2)
expected_cols = ['Index', 'demand']

shape_check = "Passed" if submission_df.shape == expected_shape else f"Failed (Shape is {submission_df.shape})"
col_check = "Passed" if list(submission_df.columns) == expected_cols else f"Failed (Cols are {list(submission_df.columns)})"

print(f"Shape Check (41778, 2): {shape_check}")
print(f"Column Check ['Index', 'demand']: {col_check}")

# 3. Save to CSV
# Using index=False is mandatory to prevent pandas from writing row numbers as an extra column
submission_filename = 'submission_autogluon_ultimate.csv'
submission_df.to_csv(submission_filename, index=False)

print(f"\nSuccess. Ultimate file saved as: {submission_filename}")
print("\nPreview of the final submission file:")
display(submission_df.head(10))
