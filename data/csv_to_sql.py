import os
import pandas as pd
import sqlite3

current_directory = os.path.dirname(os.path.abspath(__file__))
csv_file_path = os.path.join(current_directory, "tasks.csv")
df = pd.read_csv(csv_file_path)
df["due_date"] = pd.to_datetime(df["due_date"])

print(df.head())

conn = sqlite3.connect("tasks.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    task_id INTEGER PRIMARY KEY,
    task_name TEXT NOT NULL,
    due_date TIMESTAMP,
    status TEXT
)
""")

df.to_sql("tasks", conn, if_exists="replace", index=False)

conn.commit()
conn.close()

print("CSV file has been successfully converted to an SQL database.")
