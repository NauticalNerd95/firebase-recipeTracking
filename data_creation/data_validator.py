import pandas as pd
import os

OUTPUT_DIR = r"C:\Users\shalom BSC CS\Documents\DE JOURNEY\PY PROJECTS\recipeThinkbridge\output" 
RECIPES_FILE = os.path.join(OUTPUT_DIR, 'recipes.csv')
USERS_FILE = os.path.join(OUTPUT_DIR, 'users.csv')

VALID_DIFFICULTY_LEVELS = ['Easy', 'Medium', 'Hard']
REQUIRED_RECIPE_FIELDS = ['recipe_id', 'user_id', 'name', 'servings', 'difficulty', 'prep_time_min']
REQUIRED_USER_FIELDS = ['user_id', 'join_date']

MAX_COOK_TIME_MIN = 300


def load_data(filepath):
    try:
        df = pd.read_csv(filepath, dtype={'recipe_id': str, 'user_id': str})
        print(f"Loaded {len(df)} rows from {os.path.basename(filepath)}.")
        return df
    except FileNotFoundError as e:
        print(f"Error: Input file not found at {filepath}")
        print("Please ensure Module 3 (etl_pipeline.py) was run successfully and created the CSVs.")
        return pd.DataFrame()

def check_completeness(df, required_fields, entity_name):
    print(f"\n-- DQ Check: Completeness ({entity_name}) ---")
    
    missing_mask = df[required_fields].isnull().any(axis=1)
    bad_data = df[missing_mask]
    
    if not bad_data.empty:
        print(f" VIOLATION: Found {len(bad_data)} records with missing critical data.")
    else:
        print(" Passed: No critical missing data found.")
    
    return df[~missing_mask] 

def check_validity_difficulty(df):
    print("\n-- DQ Check: Validity (Difficulty Level) ---")
    
    invalid_mask = ~df['difficulty'].isin(VALID_DIFFICULTY_LEVELS)
    bad_data = df[invalid_mask]
    
    if not bad_data.empty:
        print(f"  VIOLATION: Found {len(bad_data)} records with invalid difficulty levels.")
        print(f"  Invalid values found: {bad_data['difficulty'].unique().tolist()}")
    else:
        print("  Passed: All difficulty levels are valid.")
        
    return df[~invalid_mask]

def check_consistency_times(df):
    print("\n--- DQ Check: Consistency (Cook Time) ---")
    
    inconsistent_mask = (df['cook_time_min'] <= 0) | (df['cook_time_min'] > MAX_COOK_TIME_MIN)
    bad_data = df[inconsistent_mask]
    
    if not bad_data.empty:
        print(f"VIOLATION: Found {len(bad_data)} records with inconsistent cook time values.")
    else:
        print("Passed: Cook times are consistent.")
        
    return df[~inconsistent_mask]

def save_clean_data(df, filename):
    filepath = os.path.join(OUTPUT_DIR, filename)
    df.to_csv(filepath, index=False)
    print(f"  -> Saved {len(df)} clean rows back to {filename}.")

def run_data_validation():    
    recipes_df = load_data(RECIPES_FILE)
    users_df = load_data(USERS_FILE)
    
    if recipes_df.empty or users_df.empty:
        print("Validation skipped due to missing input data.")
        return

    print("\n\n- Validating RECIPE Data ---")
    
    clean_recipes = recipes_df.copy()
    
    clean_recipes = check_completeness(clean_recipes, REQUIRED_RECIPE_FIELDS, "Recipes")
    clean_recipes = check_validity_difficulty(clean_recipes)
    final_clean_recipes = check_consistency_times(clean_recipes)
    
    final_clean_users = check_completeness(users_df.copy(), REQUIRED_USER_FIELDS, "Users")

    save_clean_data(final_clean_recipes, 'recipes.csv')
    save_clean_data(final_clean_users, 'users.csv')
    
if __name__ == '__main__':
    run_data_validation()