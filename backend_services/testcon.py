import sqlite3
import pandas as pd

from core.store_sql import SQLPipeline

# Set up SQL connection and Store patient identifier information
sqlcon = SQLPipeline()
try:
    sqlcon.create_connection()
except Exception as ex:
         print("Exception:", ex)

sqlcon.create_table()
# sqlcon.store_data(patients, 'patient')
#
#
# finally:
#     SQLCon.save_changes()
