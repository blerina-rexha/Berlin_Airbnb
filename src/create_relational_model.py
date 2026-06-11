import pandas as pd
from sqlalchemy import create_engine
import os

def build_relational_tables():
    print("=========================================")
    print("STARTING DATA MODELING (RELATIONAL MODEL)")
    print("=========================================")
    
    # 1. Read the cleaned dataset created in the first step
    cleaned_path = "data/processed/berlin_airbnb_cleaned.csv"
    if not os.path.exists(cleaned_path):
        print(f"[ERROR] Cannot find the cleaned file at {cleaned_path}!")
        print("Please run 'python src/data_cleaning_pipeline.py' first.")
        return
        
    df = pd.read_csv(cleaned_path)
    print(f"[SUCCESS] Loaded {df.shape[0]} cleaned rows.")

    # 2. Handle specific text column missing values to prevent SQL Null issues
    df['Listing Name'] = df['Listing Name'].fillna('No Name')
    df['Host Name'] = df['Host Name'].fillna('Unknown Host')
    df['Comments'] = df['Comments'].fillna('No Comment')
    df['Is Superhost'] = df['Is Superhost'].fillna('f')

    # 3. Split data into 4 relational tables based on group structure
    print("Step 2: Splitting data into 4 relational tables...")
    
    hosts_table = df[['Host ID', 'Host Name', 'Host URL', 'Host Since', 'Host Response Time', 'Host Response Rate', 'Is Superhost']].drop_duplicates(subset=['Host ID'])

    ratings_table = df[['Listing ID', 'Overall Rating', 'Accuracy Rating', 'Cleanliness Rating', 'Checkin Rating', 'Communication Rating', 'Location Rating', 'Value Rating']].drop_duplicates(subset=['Listing ID'])

    # Safeguard in case Review ID is missing from this specific chunk
    reviews_cols = ['Review ID', 'Listing ID', 'review_date', 'Reviewer ID', 'Reviewer Name', 'Comments']
    available_reviews_cols = [col for col in reviews_cols if col in df.columns]
    reviews_table = df[available_reviews_cols].drop_duplicates()

    columns_to_drop = [
        'Host Name', 'Host URL', 'Host Since', 'Host Response Time', 'Host Response Rate', 'Is Superhost',
        'Overall Rating', 'Accuracy Rating', 'Cleanliness Rating', 'Checkin Rating', 'Communication Rating', 'Location Rating', 'Value Rating',
        'Review ID', 'review_date', 'Reviewer ID', 'Reviewer Name', 'Comments'
    ]
    listings_table = df.drop(columns=columns_to_drop, errors='ignore').drop_duplicates(subset=['Listing ID'])

    # 4. Connect to your local PostgreSQL database (pgAdmin 4)
    print("Step 3: Connecting to PostgreSQL and exporting tables...")
    engine = create_engine("postgresql://postgres:Aminiki31195!@localhost:5432/Berlin_Airbnb")

    # Exporting the tables to pgAdmin 4
    hosts_table.to_sql('hosts', con=engine, if_exists='replace', index=False)
    print("- Table 'hosts' exported successfully.")
    
    ratings_table.to_sql('ratings', con=engine, if_exists='replace', index=False)
    print("- Table 'ratings' exported successfully.")
    
    if not reviews_table.empty:
        reviews_table.to_sql('reviews', con=engine, if_exists='replace', index=False)
        print("- Table 'reviews' exported successfully.")
        
    listings_table.to_sql('listings', con=engine, if_exists='replace', index=False)
    print("- Table 'listings' exported successfully.")
    
    print("=========================================")
    print("🎉 SUCCESS! The 4 relational tables are now live in pgAdmin 4!")
    print("=========================================")

if __name__ == "__main__":
    build_relational_tables()