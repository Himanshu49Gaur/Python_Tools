import pandas as pd
import os
import shutil
from autogluon.tabular import TabularPredictor
import time

print("Step 7: Deploying AutoGluon (Extreme Quality Preset with Data Merger)...")

# 1. Clean up previous failed runs to prevent the "Learner is already fit" error
ag_path = "AutogluonModels/ultimate_model"
if os.path.exists(ag_path):
    shutil.rmtree(ag_path)

# 2. Combine ALL available data 
# AutoGluon performs best when it manages its own cross-validation. 
# We merge the augmented training data and our local validation data into one massive dataset.
train_data_ag = X_trn_augmented.copy()
train_data_ag[TARGET] = y_trn_augmented

val_data_ag = X_val.copy()
val_data_ag[TARGET] = y_val

full_ag_data = pd.concat([train_data_ag, val_data_ag], axis=0).reset_index(drop=True)

print(f"Initializing AutoGluon with {len(full_ag_data)} rows of combined data...")

# 3. Initialize and Train the Predictor
# We remove 'tuning_data' so AutoGluon can perform proper 8-fold bagging across all data
predictor = TabularPredictor(
    label=TARGET, 
    eval_metric='r2',
    problem_type='regression',
    path=ag_path
).fit(
    train_data=full_ag_data,
    presets='best_quality',
    time_limit=3600, 
    verbosity=2
)

print("\nAutoGluon Training Complete.")

# 4. Display the internal cross-validation leaderboard
print("\nAutoGluon Internal Model Leaderboard:")
leaderboard = predictor.leaderboard(silent=True)
display(leaderboard)
