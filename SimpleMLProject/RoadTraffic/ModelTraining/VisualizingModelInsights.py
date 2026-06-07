import matplotlib.pyplot as plt
import seaborn as sns

print("Step 9: Visualizing AutoGluon Insights...")

# ---------------------------------------------------------
# 1. Calculate Feature Importance
# ---------------------------------------------------------
print("Calculating feature permutation importance (this takes about 30-60 seconds)...")
# We sample 10,000 rows to calculate importance quickly without timing out the notebook
sample_data = full_ag_data.sample(n=min(10000, len(full_ag_data)), random_state=42)
feature_importance = predictor.feature_importance(sample_data)

# ---------------------------------------------------------
# 2. Extract Internal Leaderboard
# ---------------------------------------------------------
leaderboard = predictor.leaderboard(silent=True)
# Keep only the top 15 models to ensure the chart is readable
top_models = leaderboard.head(15)

# ---------------------------------------------------------
# 3. Build the Visualizations
# ---------------------------------------------------------
fig = plt.figure(figsize=(20, 10))
sns.set_theme(style="whitegrid")

# Plot 1: Feature Importance
ax1 = fig.add_subplot(1, 2, 1)
sns.barplot(
    x=feature_importance['importance'], 
    y=feature_importance.index, 
    palette='viridis', 
    ax=ax1
)
ax1.set_title('1. What features drove the highest score?', fontsize=15, fontweight='bold')
ax1.set_xlabel('Permutation Importance Score (Higher is better)')
ax1.set_ylabel('Engineered Features')

# Plot 2: Internal Model Leaderboard
ax2 = fig.add_subplot(1, 2, 2)
sns.barplot(
    x=top_models['score_val'], 
    y=top_models['model'], 
    palette='magma', 
    ax=ax2
)
ax2.set_title('2. AutoGluon Internal Model Leaderboard', fontsize=15, fontweight='bold')
ax2.set_xlabel('Out-of-Fold R-squared Score')
ax2.set_ylabel('Algorithms / Stacking Ensembles')

plt.tight_layout()
plt.show()

print("Visualization complete.")
