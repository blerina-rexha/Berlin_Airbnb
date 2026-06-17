import sys
# هذه السطور هي الحل السحري لتجاهل أخطاء الترميز في النظام
sys.stdout.reconfigure(encoding='utf-8', errors='ignore')

from sqlalchemy import create_engine

# الاتصال الأساسي
engine = create_engine("postgresql://postgres:postgres@localhost:5432/Berlin_Airbnb")

try:
    with engine.connect() as conn:
        print("Success! Connection established.")
except Exception as e:
    # طباعة الخطأ بطريقة لا تسبب انهيار البرنامج بسبب الترميز
    print(f"Connection failed, but ignoring encoding errors: {str(e).encode('ascii', 'ignore').decode('ascii')}")