import pandas as pd
import os
from datetime import datetime
from data_creation.intialize_data import db 

COLLECTIONS = ["recipes", "users", "interactions"]

def extract_data(collection_name):
    """E: Fetches all documents from a specified Firestore collection."""
    if db is None:
        print(f" DB connection failed. Cannot extract data from {collection_name}.")
        return []
    
    print(f"Extraction: Fetching documents from '{collection_name}'...")
    data = []
    try:
        docs = db.collection(collection_name).stream()
        for doc in docs:
            doc_data = doc.to_dict()
            data.append(doc_data)
        print(f"  -> Extracted {len(data)} documents.")
    except Exception as e:
        print(f"Error extracting data from {collection_name}: {e}")
    
    return data

def transform_recipe_data(recipes_data):
    recipes_master = []
    ingredients = []
    steps = []
    
    print("Transformation: Flattening nested recipe data (ingredients/steps)...")
    
    for recipe in recipes_data:
        recipe_id = recipe.get('recipe_id')
        
        master_row = {
            'recipe_id': recipe_id,
            'user_id': recipe.get('user_id'),
            'name': recipe.get('name'),
            'servings': recipe.get('servings'),
            'prep_time_min': recipe.get('prep_time_min'),
            'cook_time_min': recipe.get('cook_time_min'),
            'difficulty': recipe.get('difficulty'),
            'created_at': recipe.get('created_at', datetime.now()).isoformat() 
        }
        recipes_master.append(master_row)
        
        for ingredient in recipe.get('ingredients', []):
            ingredient_row = {
                'recipe_id': recipe_id, # This is the Foreign Key (FK)
                'ingredient_name': ingredient.get('name'),
                'quantity': ingredient.get('quantity'),
                'unit': ingredient.get('unit')
            }
            ingredients.append(ingredient_row)

        # 3. STEPS TABLE 
        for step in recipe.get('steps', []):
            step_row = {
                'recipe_id': recipe_id, # This is the Foreign Key (FK)
                'step_number': step.get('step_number'),
                'instruction': step.get('instruction')
            }
            steps.append(step_row)
            
    print(f"  -> Generated {len(recipes_master)} master recipes.")
    
    return recipes_master, ingredients, steps

def load_to_csv(data_list, filename):
    if not data_list:
        print(f"Load: Skipping {filename} - No data to write.")
        return
        
    os.makedirs(r"C:\Users\shalom BSC CS\Documents\DE JOURNEY\PY PROJECTS\recipeThinkbridge\output", exist_ok=True)
    filepath = os.path.join(r"C:\Users\shalom BSC CS\Documents\DE JOURNEY\PY PROJECTS\recipeThinkbridge\output", filename)
    
    df = pd.DataFrame(data_list)
    
    df.to_csv(filepath, index=False)
    print(f"Load:  Successfully wrote {len(df)} rows to {filepath}")


def run_etl_pipeline():
    if db is None:
        print("\nPipeline Aborted: Cannot connect to Firestore. Check initialize_data.py.")
        return
        
    print("\n Starting Module 3")

    # 1. EXTRACT (E)
    raw_recipes = extract_data("recipes")
    raw_users = extract_data("users")
    raw_interactions = extract_data("interactions")

    # 2. (Tranforms) - Normalization
    recipes_master, ingredients, steps = transform_recipe_data(raw_recipes)
    
    print("\n--- Starting Load Phase ---")
    load_to_csv(recipes_master, "recipes.csv")
    load_to_csv(ingredients, "ingredients.csv")
    load_to_csv(steps, "steps.csv")
    load_to_csv(raw_users, "users.csv") 
    load_to_csv(raw_interactions, "interactions.csv") 
    
    print("\n===========")
    print("Module 3 ETL Complete. Check the output folder.")

if __name__ == "__main__":
    run_etl_pipeline()