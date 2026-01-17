import sqlite3
import pandas as pd

conn = sqlite3.connect("data/sales.db")

df = pd.read_sql_query(
    "SELECT customer_id, name FROM customers",
    conn
)

conn.close()
print(df)
