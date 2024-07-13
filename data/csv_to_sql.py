import os
import pandas as pd
import sqlite3

def populate_data():
    current_directory = os.path.dirname(os.path.abspath(__file__))
    csv_file_path = os.path.join(current_directory, "tasks.csv")
    db_file_path = os.path.join(current_directory, "tasks.db")

    df = pd.read_csv(csv_file_path)
    df["due_date"] = pd.to_datetime(df["due_date"])

    conn = sqlite3.connect(db_file_path)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        task_id TEXT PRIMARY KEY,
        task_name VARCHAR(255) NOT NULL,
        due_date TIMESTAMP,
        status VARCHAR(20)
    )
    """)

    df.to_sql("tasks", conn, if_exists="replace", index=False)

    conn.commit()
    conn.close()

    print("CSV file has been successfully converted to an SQL database.")
