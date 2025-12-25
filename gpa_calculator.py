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

def calculate_gpa(csv_path, semester=None, last_n_credits=None):
    df = pd.read_csv(csv_path)

    df = df[df['grade'] != 'W']

    if semester:
        df = df[df['semester'] == semester]
    else:
        df = df.sort_values('semester').groupby('class_name').tail(1)

    # If last_n_credits is specified, filter to most recent courses
    if last_n_credits:
        # Sort by semester descending (most recent first)
        df = df.sort_values('semester', ascending=False)
        
        # Take courses until we reach or slightly exceed the credit limit
        # This ensures we include the most recent courses
        cumulative_credits = 0
        selected_indices = []
        for idx, row in df.iterrows():
            selected_indices.append(idx)
            cumulative_credits += row['credit']
            # Stop if we've reached or exceeded the target credits
            if cumulative_credits >= last_n_credits:
                break
        
        df = df.loc[selected_indices]
        # Sort back by semester for display (most recent first)
        df = df.sort_values('semester', ascending=False)

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
    
    if last_n_credits:
        label = f"Last {last_n_credits} Credits"
    elif semester:
        label = semester
    else:
        label = "All Semesters"
    
    print(f"Weighted GPA ({label}): {weighted_gpa:.3f}")

    return weighted_gpa


def calculate_required_gpa(csv_path, target_gpa, credits_remain):
    df = pd.read_csv(csv_path)
    df = df[df['grade'] != 'W']
    df = df.sort_values('semester').groupby('class_name').tail(1)
    
    df['gpa'] = df['grade'].map(gpa_scale)
    
    if df['gpa'].isnull().any():
        print("Warning: Some grades not recognized in GPA scale and were ignored.")
    
    df['weighted_score'] = df['gpa'] * df['credit']
    
    if df.empty:
        print("No valid grades found for GPA calculation.")
        return None
    
    current_credits = df['credit'].sum()
    current_weighted_score = df['weighted_score'].sum()
    current_gpa = current_weighted_score / current_credits
    
    total_credits = current_credits + credits_remain
    target_weighted_score = target_gpa * total_credits
    
    required_weighted_score = target_weighted_score - current_weighted_score
    
    required_gpa = required_weighted_score / credits_remain
    
    print("\n" + "="*60)
    print("Required GPA Calculation:")
    print("="*60)
    print(f"Current GPA: {current_gpa:.3f}")
    print(f"Current Credits: {current_credits:.2f}")
    print(f"Target GPA: {target_gpa:.3f}")
    print(f"Credits Remaining: {credits_remain:.2f}")
    print(f"Total Credits (after completion): {total_credits:.2f}")
    print("-"*60)
    
    if required_gpa > 4.0:
        print(f"Required GPA: {required_gpa:.3f} (IMPOSSIBLE - exceeds 4.0)")
        print("You cannot achieve this target GPA with the remaining credits.")
        return None
    elif required_gpa < 0:
        print(f"Required GPA: {required_gpa:.3f} (Already achieved or exceeded)")
        print("You have already achieved or exceeded the target GPA.")
        return None
    else:
        print(f"Required GPA: {required_gpa:.3f}")
        
        closest_grade = min(gpa_scale.items(), key=lambda x: abs(x[1] - required_gpa))
        print(f"Closest Grade: {closest_grade[0]} ({closest_grade[1]:.3f})")
        
        if required_gpa > closest_grade[1]:
            next_grade = None
            for grade, gpa_val in sorted(gpa_scale.items(), key=lambda x: x[1], reverse=True):
                if gpa_val > closest_grade[1]:
                    next_grade = (grade, gpa_val)
                    break
            if next_grade:
                print(f"You need at least: {next_grade[0]} ({next_grade[1]:.3f})")
        
        return required_gpa


calculate_gpa('grades.csv')                      
# calculate_gpa('grades.csv', semester='2026spring')
# calculate_gpa('grades.csv', last_n_credits=60)
# calculate_required_gpa('grades.csv', target_gpa=3.8, credits_remain=21)  
