import pandas as pd

def analyze_student_performance():
    # 1. Embedded Data
    data = {
        'Student': ['Sam', 'Dean', 'Castiel', 'Crowley', 'Rowena', 'Jack', 'Kevin', 'Charlie'],
        'Subject': ['Math', 'Math', 'Math', 'Math', 'Science', 'Science', 'Science', 'Science'],
        'Hours_Studied': [2, 4, 3, 1, 5, 6, 8, 5],
        'Score': [65, 78, 72, 55, 88, 92, 95, 85]
    }
    
    df = pd.DataFrame(data)
    
    print("--- Full Dataset ---")
    print(df.head(10))
    print("\n")

    # 2. General Statistics
    print("--- General Statistics (Numeric) ---")
    # Describe calculates count, mean, std, min, max, and quartiles
    print(df.describe())
    print("\n")

    # 3. Grouped Analysis
    print("--- Average Score by Subject ---")
    subject_stats = df.groupby('Subject')[['Score', 'Hours_Studied']].mean()
    print(subject_stats)
    
    # 4. Finding Extremes
    top_student = df.loc[df['Score'].idxmax()]
    print(f"\n--- Top Performing Student ---\n{top_student['Student']} with {top_student['Score']} points.")

if __name__ == "__main__":
    analyze_student_performance()
