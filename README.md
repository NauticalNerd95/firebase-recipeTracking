# MyRecipe ETL & Analytics Project

##  Overview of the project

This project is a complete **end-to-end ETL (Extract–Transform–Load) Data Engineering Pipeline** for analyzing user recipes. It takes data created by users in a Firebase Firestore backend and moves it across:

1. **Firestore Database**
2. **Local Python ETL Process**
3. **Validated CSV files**
4. **Google Sheets using Google Sheets API**
5. **Looker Studio for visual dashboards and insights**

This pipeline demonstrates how raw data from a live application can be:

- Extracted from a real database  
- Cleaned, validated, and structured  
- Loaded into analytics-friendly storage  
- Visualized for business insights

---

## 🎯 Project Goals

- Collect user recipe submissions (name, ingredients, prep time, steps, etc.) from Firestore  
- Convert Firestore recipe objects into structured CSV format  
- Validate the data  
- Automatically upload structured data to Google Sheets  
- Connect Google Sheets to Looker Studio  
- Build dashboards analyzing:
  - Most liked recipes  
  - Ingredient trends  
  - Time to prepare vs popularity  
  - User contribution metrics

---

## 🧠 Architecture

Firestore → Python ETL → CSV Files → Google Sheets → Looker Studio Dashboards

Here is the directory strucuture for my project
<img width="438" height="559" alt="image" src="https://github.com/user-attachments/assets/c41f9bde-6c41-4d2c-86f4-9ae924269b75" />

---

## 📂 CSV Output Files

The ETL produces four structured datasets:

| File | Description |
|---|---|
| `recipes.csv` | Master recipe information |
| `ingredients.csv` | Each ingredient linked to a recipe |
| `steps.csv` | Ordered cooking steps |
| `interactions.csv` | Likes, ratings, and user engagement |
| `users.csv` | Information about the users and their activity |

---

## 🏗️ How the Pipeline Works

### 1️⃣ Extract – Firestore
The system connects to Firebase Firestore using the service key JSON and retrieves recipe documents.

📷 *<img width="1361" height="643" alt="image" src="https://github.com/user-attachments/assets/ee25d62e-6fd4-4609-8797-698c2ecae09b" />*

---

### 2️⃣ Transform – In Python

Data transformations include:

- Flattening nested Firestore JSON structures  
- Ensuring proper data types  
- Cleaning missing values  
- Generating unique IDs (UUIDs)  
- Converting arrays (steps, ingredients) into normalized rows

*HERE IS SOME SNIPPET OF ETL CODE*
```python
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
```

---

### 3️⃣ Load – Write to CSV

Each dataset is written into individual CSV files locally:

recipes.csv
ingredients.csv
steps.csv
interactions.csv

*<img width="369" height="133" alt="image" src="https://github.com/user-attachments/assets/1ee7c707-2f0b-4723-85ae-5e6bdf3d22c0" />*
---

### 4️⃣ Upload to Google Sheets

Using the Google Sheets API:

- Each CSV is automatically uploaded (using service account of GCP and enabling google sheets api)
- Each file becomes a worksheet  
- Data replaces previous records cleanly

*<img width="1286" height="640" alt="image" src="https://github.com/user-attachments/assets/642426a2-415e-4756-8cc2-584b82be55b5" />
*
---

### 5️⃣ Visualization in Looker Studio

Google Sheets is selected as a data source in Looker Studio.

Dashboards include:

- **Average prep time vs rating**
- **User contribution leaderboard**
- **Most common ingredients**
- **Recipe engagement analysis**

 *<img width="1357" height="633" alt="image" src="https://github.com/user-attachments/assets/fa0682bf-4667-4e9a-a6c7-e5c0b3b5de3a" />
*
---

## 📊 Example Insights

- Some long preparation recipes score highly  
- A subset of ingredients appears in majority of dishes  
- Top contributors submit more liked recipes  
- Clear correlation between preparation time and likability

---

## 🧩 ERD (Entity Relationship Diagram)

Below is the conceptual ERD of the MyRecipe Data Warehouse:

📷 *<img width="530" height="427" alt="image" src="https://github.com/user-attachments/assets/38a3fa03-1d7a-405f-9f0b-dec4a88b148c" />
*
---

## 🚀 Requirements

### 🔧 Technical Requirements

- Python 3.8+
- Firebase Firestore access
- `serviceAccountKey.json` downloaded from Firebase
- Google Cloud project with Sheets API enabled
- Google OAuth credentials for Sheets access

### 📦 Python Dependencies

firebase-admin
google-auth
google-auth-oauthlib
google-api-python-client
pandas
uuid

### 🗄️ Permissions Needed

- Read access to Firestore database
- Write access to Google Sheets
---

## ⚙️ Setup Instructions

### 1️⃣ Clone the repository

git clone https://github.com/
<your-username>/<your-repo>.git
cd <your-repo>


---

### 3️⃣ Install dependencies
pip install -r requirements.txt
---

### 4️⃣ Enable Google Sheets API

Go to:

Google Cloud Console → APIs & Services → Enable APIs → Google Sheets API


📷 *<img width="1236" height="400" alt="image" src="https://github.com/user-attachments/assets/e111524e-1b6e-445b-aefc-a15a71025a66" />
*

Download your OAuth credentials as:
credentials.json

This will:
- Read from Firestore  
- Generate CSV files  
- Upload them to Google Sheets

---

### 6️⃣ Connect Looker Studio

Looker Studio → Create → Data Source → Google Sheets → Select uploaded file


Then create reports with charts such as:

- **Scatter plot** → Prep Time vs Likes  
- **Bar graph** → Top Ingredients  
- **Leaderboard** → Top Users

---

## 🧪 Data Validation Steps

The pipeline performs:

- Null value checks  
- Type consistency  
- Duplicate avoidance  
- Referential integrity checks  
- UUID assignment for primary keys

---

## 📁 Project Structure

/
|-- etl.py
|-- serviceAccountKey.json
|-- credentials.json
|-- data/
| |-- recipes.csv
| |-- ingredients.csv
| |-- steps.csv
| |-- interactions.csv
|-- README.md


---

## 🥇 Why This Project Matters

This project demonstrates **real Data Engineering skills**, including:

- Real-world ETL pipelines  
- Working with cloud APIs  
- Data cleaning & normalization  
- Schema design  
- BI dashboarding  
- Automated repeatable analytics

---

## 📌 Future Improvements

- Schedule automated ETL using Prefect or Airflow  
- Migrate storage to BigQuery  
- Implement dbt transformations  
- Add CI/CD pipeline  
- Deploy Looker dashboards publicly
---

## 🙌 Author

**Shalom Salve**  
Apprentice Data Engineer (thinkbridge)
---

## If You Like This Project

Please ⭐ the repository on GitHub. It helps a lot!
