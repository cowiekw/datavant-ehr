import sqlite3
import pandas as pd

from core.store_sql import SQLPipeline

# Set up SQL connection and Store patient identifier information
sqlcon = SQLPipeline()
sqlcon.create_connection()
cur = sqlcon.conn.cursor()
cur.execute("SELECT first_name, last_name, state FROM patients")

patient_rows = cur.fetchall()
print("row:", patient_rows)
sqlcon.save_changes()
