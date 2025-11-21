import gspread, pandas as pd, os
from google.oauth2.service_account import Credentials
from pathlib import Path

scopes = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_file("recipes-analysis-2cf82c6fcb8d.json", scopes = scopes)

client = gspread.authorize(creds)

sheet_id = "1jpJoci7hGyIloQ9LOnu6H30wLkZyj_-mlcLLAZLBV0I"
sheet = client.open_by_key(sheet_id)

# values_list = sheet.sheet1.row_values(1)
# print(values_list)

csv_folder = r"C:\Users\shalom BSC CS\Documents\DE JOURNEY\PY PROJECTS\recipeThinkbridge\output"

# CSV file names
csv_files = ["ingredients.csv", "interactions.csv", "recipes.csv","steps.csv","users.csv"]

def upload_csv_to_sheet(csv_path, sheet_name):
    
    df = pd.read_csv(csv_path)
    df = df.replace([float("inf"), float("-inf")], None)
    df = df.fillna("")
    print(f"Reading {csv_path}: {len(df)} rows, {len(df.columns)} columns")
    
    try:
        worksheet = sheet.worksheet(sheet_name)
        print(f"Found existing sheet: {sheet_name}")
        worksheet.clear() 
    except gspread.WorksheetNotFound:
        worksheet = sheet.add_worksheet(title=sheet_name, rows=1000, cols=20)
        print(f"Created new sheet: {sheet_name}")
    
    data = [df.columns.values.tolist()] + df.values.tolist()
    
    worksheet.update(data, value_input_option='USER_ENTERED')
    print(f"✓ Uploaded {len(df)} rows to '{sheet_name}'")
    print(f"  URL: {worksheet.url}\n")
    

for csv_file in csv_files:
    csv_path = os.path.join(csv_folder, csv_file)
    
    if os.path.exists(csv_path):
        sheet_name = Path(csv_file).stem
        upload_csv_to_sheet(csv_path, sheet_name)
    else:
        print(f"⚠ Warning: {csv_path} not found, skipping...")

print("All CSV files processed!")
