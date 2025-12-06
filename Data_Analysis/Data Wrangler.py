import pandas as pd
import numpy as np

def clean_data():
    # 1. Embedded Raw Data (Simulating a messy CSV)
    raw_data = {
        'EmployeeID': [101, 102, 103, 101, 105, 106, None],
        'Name': ['Alice', 'Bob', 'Charlie', 'Alice', 'Eve', 'Frank', 'Grace'],
        'Department': ['HR', 'IT', 'Finance', 'HR', 'IT', None, 'Finance'],
        'Salary': [50000, 60000, 75000, 50000, np.nan, 55000, 72000],
        'JoiningDate': ['2020-01-15', '2019-05-20', '2018-08-10', '2020-01-15', '2021-03-12', '2020-11-01', '2019-12-05']
    }

    print("--- 1. Raw Data ---")
    df = pd.DataFrame(raw_data)
    print(df)
    print("\n")

    # 2. Data Wrangling Steps
    
    # Remove duplicates based on EmployeeID (keeping the first occurrence)
    df_cleaned = df.drop_duplicates(subset=['EmployeeID'], keep='first')
    
    # Handle Missing Values
    # Fill missing Salary with the median salary
    median_salary = df_cleaned['Salary'].median()
    df_cleaned['Salary'] = df_cleaned['Salary'].fillna(median_salary)
    
    # Fill missing Department with 'Unknown'
    df_cleaned['Department'] = df_cleaned['Department'].fillna('Unknown')
    
    # Drop rows where EmployeeID is NaN (critical missing info)
    df_cleaned = df_cleaned.dropna(subset=['EmployeeID'])
    
    # Convert types (EmployeeID to integer)
    df_cleaned['EmployeeID'] = df_cleaned['EmployeeID'].astype(int)

    print("--- 2. Cleaned Data ---")
    print(df_cleaned)
    print("\n--- 3. Summary ---")
    print(f"Original Rows: {len(df)}")
    print(f"Cleaned Rows: {len(df_cleaned)}")

if __name__ == "__main__":
    clean_data()
