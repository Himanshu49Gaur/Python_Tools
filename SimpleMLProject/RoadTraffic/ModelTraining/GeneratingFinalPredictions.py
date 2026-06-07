import numpy as np

print("Step 10: Generating Final AutoGluon Predictions on Official Test Set...")

# 1. Generate Predictions using the AutoGluon Predictor
# AutoGluon automatically selects the best weighted ensemble from its internal leaderboard
test_predictions_ag = predictor.predict(X_test)

# 2. Post-Processing (Clipping)
# We ensure no negative traffic demand predictions are submitted
test_predictions_ag = np.clip(test_predictions_ag, a_min=0, a_max=None)

print(f"Successfully generated {len(test_predictions_ag)} final predictions.")
print("\nPreview of first 5 predictions:")
print(test_predictions_ag[:5].values)
