import pandas as pd
from sqlalchemy import create_engine

df = pd.read_csv("data/raw/berlin_airbnb.csv")

engine = create_engine(
    "postgresql://postgres:Abcd!@localhost:5432/Berlin_Airbnb"
)

df.to_sql(
    "airbnb_raw",
    engine,
    if_exists="replace",
    index=False
)

print("Data imported successfully!")