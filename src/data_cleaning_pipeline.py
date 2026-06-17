import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import os

def run_data_cleaning():
    print("=========================================")
    print("STARTING THE DATA CLEANING PIPELINE")
    print("=========================================")
    
    # 1. Database Connection (مع إضافة حماية الترميز)
    engine = create_engine("postgresql://postgres:postgres@localhost:5432/Berlin_Airbnb", 
                           connect_args={"options": "-c client_encoding=LATIN1"})
    
    print("Step 1: Reading raw data from pgAdmin 4 (airbnb_raw)...")
    try:
        df = pd.read_sql("SELECT * FROM airbnb_raw", engine)
        
        # حماية إضافية: تحويل أي أحرف غير مفهومة لترميز UTF-8
        for col in df.select_dtypes(include=['object']).columns:
            df[col] = df[col].apply(lambda x: str(x).encode('latin-1', 'ignore').decode('utf-8', 'ignore'))
            
        print(f"[SUCCESS] Loaded {df.shape[0]} rows from the database.")
    except Exception as e:
        print(f"[ERROR] Could not read from database: {e}")
        return
    
    # 2. Drop the 93% empty column
    print("Step 2: Dropping 'Square Feet' column...")
    df = df.drop(columns=['Square Feet'], errors='ignore')
    
    # 3. Clean Price column
    print("Step 3: Cleaning 'Price' column...")
    if 'Price' in df.columns:
        if df['Price'].dtype == 'object':
            df['Price'] = df['Price'].astype(str).str.replace(r'[^\d.]', '', regex=True)
        df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
    
    # 4. Remove missing critical rows
    print("Step 4: Removing rows with missing Price or Listing ID...")
    df = df.dropna(subset=['Price', 'Listing ID'])
    df = df[df['Price'] > 0]
    
    # 5. Impute missing values with Median
    print("Step 5: Imputing missing columns with median...")
    columns_to_fill = ['Bathrooms', 'Bedrooms', 'Beds', 'Overall Rating', 'Reviews']
    for col in columns_to_fill:
        if col in df.columns:
            median_val = df[col].median()
            df[col] = df[col].fillna(median_val)
            
    # 6. Save to data/processed folder
    print("Step 6: Saving the cleaned dataset...")
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_path = os.path.join(base_dir, "data", "processed", "berlin_airbnb_cleaned.csv")
    
    df.to_csv(output_path, index=False)
    print("=========================================")
    print(f"SUCCESS! Cleaned file saved at:\n{output_path}")
    print(f"Final rows remaining: {df.shape[0]}")
    print("=========================================")

if __name__ == "__main__":
    run_data_cleaning()