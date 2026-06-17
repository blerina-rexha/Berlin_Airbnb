import psycopg2
import os

# تعطيل أي إعدادات محلية قد تسبب مشاكل
os.environ["LC_ALL"] = "C"
os.environ["LANG"] = "C"

try:
    # استخدام كلمة سر بسيطة والتأكد من عدم وجود رموز
    conn = psycopg2.connect(
        dbname="Berlin_Airbnb",
        user="postgres",
        password="postgres",
        host="127.0.0.1", # استخدام IP بدلاً من localhost
        port="5432"
    )
    print("نجح الاتصال!")
    conn.close()
except Exception as e:
    print(f"الخطأ هو: {e}")