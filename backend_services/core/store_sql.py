import sqlite3
import os
from core.patient import Patient

class SQLPipeline:
    """ A patient class"""
    def __init__(self, name = 'patients'):
        self.conn = None
        self.db_name = name
        self.last_post_id = 0

    def create_connection(self, erase_first=False):
        print("SQL connection created")
        self.conn = sqlite3.connect(('{0}.db').format(self.db_name))
        self.conn.row_factory = sqlite3.Row

    def create_table(self):
        cur= self.conn.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS patients
        (id INTEGER, first_name TEXT, last_name TEXT, birthday TEXT,
        address TEXT, city TEXT, state TEXT, PRIMARY KEY(id))
        """)
        print("patients table created")

        cur.execute("""CREATE TABLE IF NOT EXISTS patient_sales
        (id INT, patient_id INT
        sales_count INT, PRIMARY KEY(id), FOREIGN KEY(patient_id) REFERENCES patients (id))
        """)
        print("patient sales table created")

    def store_patient_data(self, pat, table_name):
        self.conn.row_factory = sqlite3.Row
        cur = self.conn.cursor()
        if table_name == 'patient' or table_name == 'patients':
            query = '''INSERT INTO patients (first_name, last_name, birthday, address, city, state) VALUES(?, ?, ?, ?, ?, ?)'''
            data = (pat.first_name, pat.last_name, pat.birthday, pat.address, pat.city, pat.state)
            cur.execute(query, data)
            print(pat.last_name, ": patient info was stored in table")

    def store_patient_sales(self, patients_list, sales_list):
        cur = self.conn.cursor()
        for pat in patients:
            cur.execute('''INSERT INTO patient_sales (patient_id, sales_count) VALUES (?, ?)''', pat.id, sales_count)

    def save_changes(self):
        self.conn.commit()
        self.conn.close()
