import pandas as pd

gpa_scale = {
    'A': 4.000,
    'A-': 3.667,
    'B+': 3.333,
    'B': 3.000,
    'B-': 2.667,
    'C+': 2.333,
    'C': 2.000,
    'C-': 1.667,
    'D+': 1.333,
    'D': 1.000,
    'F': 0.000
}

def calculate_gpa(csv_path, semester=None):
    df = pd.read_csv(csv_path)

    df = df[df['grade'] != 'W']

    if semester:
        df = df[df['semester'] == semester]
    else:
        df = df.sort_values('semester').groupby('class_name').tail(1)

    df['gpa'] = df['grade'].map(gpa_scale)

    if df['gpa'].isnull().any():
        print("Warning: Some grades not recognized in GPA scale and were ignored.")

    df['weighted_score'] = df['gpa'] * df['credit']

    if df.empty:
        print("No valid grades found for GPA calculation.")
        return None
    total_credits = df['credit'].sum()
    weighted_gpa = df['weighted_score'].sum() / total_credits

    print("\nGPA Calculation Result:")
    print(df[['class_name', 'semester', 'grade', 'credit', 'gpa', 'weighted_score']])
    print(f"\nTotal Credits: {total_credits:.2f}")
    print(f"Weighted GPA ({'All Semesters' if not semester else semester}): {weighted_gpa:.3f}")

    return weighted_gpa


calculate_gpa('grades.csv')                      
calculate_gpa('grades.csv', semester='2025Spring')  
