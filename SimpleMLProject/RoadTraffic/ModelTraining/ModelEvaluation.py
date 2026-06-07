print("Step 8: Evaluating AutoGluon (Internal Cross-Validation)...")

# 1. Extract the leaderboard
leaderboard = predictor.leaderboard(silent=True)

# 2. Get the R-squared score of the absolute best model (usually the top WeightedEnsemble)
best_score_r2 = leaderboard.iloc[0]['score_val']

# 3. Calculate Custom Competition Score
ag_comp_score = max(0, 100 * best_score_r2)

print("-" * 55)
print(f"{'Model':<30} | {'Comp Score':<10}")
print("-" * 55)
print(f"{'AutoGluon Ultimate Ensemble':<30} | {ag_comp_score:<10.2f}")
print("-" * 55)

if ag_comp_score >= 98:
    print("\nTarget Achieved! The AutoGluon ensemble has successfully breached the threshold.")
else:
    print(f"\nAlgorithmic maximum reached at {ag_comp_score:.2f}.")
