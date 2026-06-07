import matplotlib.pyplot as plt
import seaborn as sns

print("Starting Exploratory Data Analysis (EDA)...")

# Set the visual style for seaborn
sns.set_theme(style="whitegrid")

# Create a large figure to hold all our subplots
fig = plt.figure(figsize=(20, 30))

# ---------------------------------------------------------
# 1. Histogram / KDE Plot: Distribution of Target (demand)
# ---------------------------------------------------------
ax1 = fig.add_subplot(4, 2, 1)
sns.histplot(data=train_df, x='demand', kde=True, bins=50, color='blue', ax=ax1)
ax1.set_title('1. Distribution of Traffic Demand', fontsize=14, fontweight='bold')
ax1.set_xlabel('Demand')
ax1.set_ylabel('Frequency')

# ---------------------------------------------------------
# 2. Boxplot: Demand across Number of Lanes
# ---------------------------------------------------------
ax2 = fig.add_subplot(4, 2, 2)
sns.boxplot(data=train_df, x='NumberofLanes', y='demand', palette='Set2', ax=ax2)
ax2.set_title('2. Traffic Demand by Number of Lanes', fontsize=14, fontweight='bold')

# ---------------------------------------------------------
# 3. Barplot: Average Demand by Weather Conditions
# ---------------------------------------------------------
ax3 = fig.add_subplot(4, 2, 3)
sns.barplot(data=train_df, x='Weather', y='demand', palette='viridis', errorbar=None, ax=ax3)
ax3.set_title('3. Average Demand per Weather Condition', fontsize=14, fontweight='bold')
ax3.tick_params(axis='x', rotation=45)

# ---------------------------------------------------------
# 4. Scatterplot: Temperature vs. Demand
# ---------------------------------------------------------
ax4 = fig.add_subplot(4, 2, 4)
sns.scatterplot(data=train_df, x='Temperature', y='demand', alpha=0.3, color='coral', ax=ax4)
ax4.set_title('4. Temperature vs. Traffic Demand', fontsize=14, fontweight='bold')

# ---------------------------------------------------------
# 5. Countplot: Frequency of Different Road Types
# ---------------------------------------------------------
ax5 = fig.add_subplot(4, 2, 5)
sns.countplot(data=train_df, x='RoadType', palette='magma', ax=ax5, order=train_df['RoadType'].value_counts().index)
ax5.set_title('5. Frequency of Road Types', fontsize=14, fontweight='bold')
ax5.tick_params(axis='x', rotation=45)

# ---------------------------------------------------------
# 6. Violin Plot: Demand Distribution by Large Vehicles Allowance
# ---------------------------------------------------------
ax6 = fig.add_subplot(4, 2, 6)
sns.violinplot(data=train_df, x='LargeVehicles', y='demand', palette='coolwarm', split=True, ax=ax6)
ax6.set_title('6. Demand based on Large Vehicle Access', fontsize=14, fontweight='bold')

# ---------------------------------------------------------
# 7. Heatmap: Correlation Matrix of Numerical Features
# ---------------------------------------------------------
ax7 = fig.add_subplot(4, 2, 7)
# Select only numerical columns for the correlation matrix
numeric_cols = train_df.select_dtypes(include=['int64', 'float64']).columns
corr_matrix = train_df[numeric_cols].corr()

sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5, ax=ax7)
ax7.set_title('7. Correlation Heatmap of Numerical Features', fontsize=14, fontweight='bold')

# Hide the empty 8th subplot area
fig.add_subplot(4, 2, 8).axis('off')

# Adjust layout to prevent overlap
plt.tight_layout()
plt.show()

print("EDA completed!")
