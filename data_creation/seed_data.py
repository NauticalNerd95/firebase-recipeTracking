from datetime import datetime
import uuid
import random
from time import sleep

from data_creation.intialize_data import db
def generate_recipe_id():
    
    return str(uuid.uuid4())

def generate_user_id(prefix="user_"):
    return prefix + str(uuid.uuid4())[:8]

def get_french_toast_data(user_id):

    return {
        "recipe_id": "recipe_ft_001", 
        "user_id": user_id,
        "name": "Classic Golden French Toast",
        "description": "A simple and delicious French Toast recipe, perfect for a quick breakfast.",
        "servings": 2,
        "prep_time_min": 10,
        "cook_time_min": 8,
        "difficulty": "Easy", # Enforcing consistency for later DQ check
        "created_at": datetime.now(),
        # Denormalized ingredients and steps are kept as arrays for efficient app reading
        "ingredients": [
            {"name": "Thick White Bread", "quantity": 4, "unit": "slices"},
            {"name": "Eggs", "quantity": 3, "unit": "large"},
            {"name": "Cinnamon Powder", "quantity": 0.5, "unit": "tablespoon"},
            {"name": "Honey", "quantity": 1, "unit": "tablespoon"},
            {"name": "Butter", "quantity": 1, "unit": "spoon/pat"},
            {"name": "Milk", "quantity": 100, "unit": "ml"},
        ],
        "steps": [
            {"step_number": 1, "instruction": "Break 3 eggs into a small bowl, ensuring no shell fragments."},
            {"step_number": 2, "instruction": "Add 100 ml lukewarm milk, 0.5 tbsp cinnamon powder, and 1 tbsp honey."},
            {"step_number": 3, "instruction": "Whisk and mix all contents lightly and well."},
            {"step_number": 4, "instruction": "Place saucepan on medium heat, add 1 spoon of butter, and let it melt."},
            {"step_number": 5, "instruction": "Dip one slice of bread into the batter, ensuring all sides are evenly soaked."},
            {"step_number": 6, "instruction": "Place soaked bread on the hot pan and toast for about 1 minute per side until golden brown."},
            {"step_number": 7, "instruction": "Remove toast and repeat steps 5 and 6 for the remaining slices."},
            {"step_number": 8, "instruction": "Serve on a plate, drizzle with remaining honey, and dust with cinnamon powder."},
        ],
    }

def generate_synthetic_recipes(num_recipes, user_ids):
    """Generates a list of synthetic recipe documents (19 records)."""
    recipes = []
    recipe_names = ["Veggie Stir Fry", "Simple Pasta", "Overnight Oats", 
                    "Spicy Lentil Soup", "Chocolate Chip Cookies", "Tuna Sandwich"]
    difficulties = ["Easy", "Medium", "Hard", "Advanced"] # Add 'Advanced' to test normalization later
    
    for i in range(num_recipes):
        recipe_id = generate_recipe_id()
        prep_time = random.randint(1, 30)
        cook_time = random.randint(5, 60)
        
        recipe = {
            "recipe_id": recipe_id,
            "user_id": random.choice(user_ids),
            "name": f"{random.choice(recipe_names)} #{i+2}",
            "description": f"A synthetic recipe for quick preparation.",
            "servings": random.randint(1, 8),
            "prep_time_min": prep_time,
            "cook_time_min": cook_time,
            "difficulty": random.choice(difficulties),
            "created_at": datetime.now(),
            "ingredients": [{"name": f"synthetic_item_{j}", "quantity": random.uniform(0.5, 5), "unit": random.choice(['cup', 'g', 'ml', 'unit'])} for j in range(random.randint(2, 6))],
            "steps": [{"step_number": j, "instruction": f"Synthetic step {j}."} for j in range(1, random.randint(3, 8))],
        }
        recipes.append(recipe)
        
    return recipes

def generate_interactions(recipe_ids, user_ids, num_interactions=100):
    interactions = []
    interaction_types = ["view", "like", "cook_attempt", "rating"]
    
    for i in range(num_interactions):
        interaction_type = random.choice(interaction_types)
        value = None
        
        if interaction_type == "rating":
            # Rating between 1.0 and 5.0
            value = round(random.uniform(1.0, 5.0), 1) 
        
        # Simulate interaction time over the last 30 days
        interaction_time = datetime.now().timestamp() - random.randint(1, 86400 * 30) 
        
        interaction = {
            "interaction_id": generate_recipe_id(),
            "user_id": random.choice(user_ids),
            "recipe_id": random.choice(recipe_ids),
            "interaction_type": interaction_type,
            "timestamp": datetime.fromtimestamp(interaction_time),
            "value": value,
        }
        interactions.append(interaction)
        sleep(0.005) # Small delay to ensure unique timestamps
        
    return interactions


def seed_firestore_data():
    """Main function to seed all data into Firestore collections."""
    if db is None:
        print("🚨 Cannot seed data: Firebase client is not initialized.")
        return

    print("\n--- 1. Setting up Users (3 Records) ---")
    
    my_user_id = generate_user_id("creator_")
    synthetic_user_ids = [generate_user_id("synth_") for _ in range(2)]
    all_user_ids = [my_user_id] + synthetic_user_ids
    
    users_data = [
        {"user_id": my_user_id, "join_date": datetime(2023, 1, 1), "region": "North America"},
        {"user_id": synthetic_user_ids[0], "join_date": datetime(2023, 3, 15), "region": "Europe"},
        {"user_id": synthetic_user_ids[1], "join_date": datetime(2023, 5, 20), "region": "Asia"},
    ]
    
    for user_doc in users_data:
        db.collection("users").document(user_doc["user_id"]).set(user_doc)
        print(f"  -> Added User: {user_doc['user_id']}")
    
    print("\n--- 2. Setting up Recipes (20 Total) ---")

    my_recipe = get_french_toast_data(my_user_id)
    all_recipes = [my_recipe]
    
    synthetic_recipes = generate_synthetic_recipes(19, all_user_ids)
    all_recipes.extend(synthetic_recipes)
    
    recipe_ids = []
    for recipe_doc in all_recipes:
        doc_ref = db.collection("recipes").document(recipe_doc["recipe_id"])
        doc_ref.set(recipe_doc)
        recipe_ids.append(recipe_doc["recipe_id"])
        print(f"  -> Added Recipe: {recipe_doc['name']} ({recipe_doc['recipe_id']})")

    print("\n--- 3. Setting up Interactions (100 Total) ---")
    
    interactions = generate_interactions(recipe_ids, all_user_ids, num_interactions=100)
    
    for interaction_doc in interactions:
        # Use interaction_id as the Document ID
        db.collection("interactions").document(interaction_doc["interaction_id"]).set(interaction_doc)
        
    print(f"  -> Added {len(interactions)} synthetic interactions.")
    
    print("\n=======================================================")
    print("Module 2: Firestore Data Seeding Complete!")
    print("Run the command: python -m data.firestore_seeder")
    print("=======================================================")

if __name__ == "__main__":
    seed_firestore_data()