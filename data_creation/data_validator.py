import pandas as pd
import os

# Define paths for the clean data files
# We use a simple relative path 'output', which works seamlessly
# when the script is executed using 'python -m ...' from the project root.
OUTPUT_DIR = r"C:\Users\shalom BSC CS\Documents\DE JOURNEY\PY PROJECTS\recipeThinkbridge\output" 
RECIPES_FILE = os.path.join(OUTPUT_DIR, 'recipes.csv')
USERS_FILE = os.path.join(OUTPUT_DIR, 'users.csv')

# --- Data Quality Rule Definitions ---
# 1. VALIDITY: Difficulty must be one of these defined values.
VALID_DIFFICULTY_LEVELS = ['Easy', 'Medium', 'Hard']

# 2. COMPLETENESS: These columns must not have missing (null) values.
REQUIRED_RECIPE_FIELDS = ['recipe_id', 'user_id', 'name', 'servings', 'difficulty', 'prep_time_min']
REQUIRED_USER_FIELDS = ['user_id', 'join_date']

# 3. CONSISTENCY: Cook times should be positive and within a reasonable limit.
MAX_COOK_TIME_MIN = 300 # 5 hours maximum for consistency check

# -------------------------------------

def load_data(filepath):
    """Loads a CSV file into a Pandas DataFrame."""
    try:
        # We read the ID columns as strings for consistency
        df = pd.read_csv(filepath, dtype={'recipe_id': str, 'user_id': str})
        print(f"Loaded {len(df)} rows from {os.path.basename(filepath)}.")
        return df
    except FileNotFoundError as e:
        print(f"❌ Error: Input file not found at {filepath}")
        print("Please ensure Module 3 (etl_pipeline.py) was run successfully and created the CSVs.")
        return pd.DataFrame()

def check_completeness(df, required_fields, entity_name):
    """Checks for missing (null) values in required columns (Completeness Rule)."""
    print(f"\n--- DQ Check: Completeness ({entity_name}) ---")
    
    # Identify rows where ANY of the required fields are null (True if missing)
    missing_mask = df[required_fields].isnull().any(axis=1)
    bad_data = df[missing_mask]
    
    if not bad_data.empty:
        print(f"  🚨 VIOLATION: Found {len(bad_data)} records with missing critical data.")
    else:
        print("  ✅ Passed: No critical missing data found.")
    
    # Return data where the mask is False (i.e., data that is NOT missing)
    return df[~missing_mask] 

def check_validity_difficulty(df):
    """Checks if the 'difficulty' field contains only valid, expected values (Validity Rule)."""
    print("\n--- DQ Check: Validity (Difficulty Level) ---")
    
    # Identify rows where 'difficulty' is NOT in the list of valid levels
    invalid_mask = ~df['difficulty'].isin(VALID_DIFFICULTY_LEVELS)
    bad_data = df[invalid_mask]
    
    if not bad_data.empty:
        print(f"  🚨 VIOLATION: Found {len(bad_data)} records with invalid difficulty levels.")
        print(f"    Invalid values found: {bad_data['difficulty'].unique().tolist()}")
    else:
        print("  ✅ Passed: All difficulty levels are valid.")
        
    # Return data where the mask is False (i.e., data that IS valid)
    return df[~invalid_mask]

def check_consistency_times(df):
    """Checks if cook times are positive and within a reasonable limit (Consistency Rule)."""
    print("\n--- DQ Check: Consistency (Cook Time) ---")
    
    # Check for non-positive or excessively long times
    inconsistent_mask = (df['cook_time_min'] <= 0) | (df['cook_time_min'] > MAX_COOK_TIME_MIN)
    bad_data = df[inconsistent_mask]
    
    if not bad_data.empty:
        print(f"  🚨 VIOLATION: Found {len(bad_data)} records with inconsistent cook time values.")
    else:
        print("  ✅ Passed: Cook times are consistent.")
        
    return df[~inconsistent_mask]

def save_clean_data(df, filename):
    """Saves the cleaned DataFrame back to the output directory, overwriting the old CSV."""
    # Uses the globally defined OUTPUT_DIR
    filepath = os.path.join(OUTPUT_DIR, filename)
    # Ensure the index is not written as a column
    df.to_csv(filepath, index=False)
    print(f"  -> Saved {len(df)} clean rows back to {filename}.")

def run_data_validation():
    """Main function to orchestrate the data quality checks."""
    print("\n--- Starting Module 4: Data Quality Validation ---")
    
    # 1. LOAD DATA
    recipes_df = load_data(RECIPES_FILE)
    users_df = load_data(USERS_FILE)
    
    if recipes_df.empty or users_df.empty:
        print("Validation skipped due to missing input data.")
        return

    # 2. RECIPE DATA VALIDATION & CLEANING
    print("\n\n--- Validating RECIPE Data ---")
    
    # Apply checks sequentially, cleaning data at each step
    clean_recipes = recipes_df.copy()
    
    clean_recipes = check_completeness(clean_recipes, REQUIRED_RECIPE_FIELDS, "Recipes")
    clean_recipes = check_validity_difficulty(clean_recipes)
    final_clean_recipes = check_consistency_times(clean_recipes)
    
    # 3. USER DATA VALIDATION & CLEANING
    print("\n\n--- Validating USER Data ---")
    # Users only need a completeness check in this simple pipeline
    final_clean_users = check_completeness(users_df.copy(), REQUIRED_USER_FIELDS, "Users")

    # 4. SAVE CLEAN DATA
    print("\n\n--- Saving Clean Data ---")
    save_clean_data(final_clean_recipes, 'recipes.csv')
    save_clean_data(final_clean_users, 'users.csv')
    
    print("\n=======================================================")
    print("✅ Module 4 Data Quality Complete.")
    print("Next Step: Run analytics_engine.py (Module 5).")
    print("=======================================================")

if __name__ == '__main__':
    run_data_validation()