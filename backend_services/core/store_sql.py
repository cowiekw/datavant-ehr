import sqlite3
import os
from core.patient import Patient

class SQLPipeline:
    """ A patient class"""
    def __init__(self, name = 'patientsdb'):
        self.conn = None
        self.db_name = name
        self.last_post_id = 0

    def create_connection(self, erase_first=False):
        print("SQL connection created")
        self.conn = sqlite3.connect(('{0}.db').format(self.db_name))
        db  = self.conn.cursor()

    def create_table(self):
        db = self.conn.cursor()
        db.execute("""DROP TABLE IF EXISTS patients""")
        db.execute("""CREATE TABLE patients
        (id INTEGER, first_name TEXT, last_name TEXT,
        address TEXT, city TEXT, state TEXT, sales_count INT, PRIMARY KEY(id))
        """)
        print("patients table created")
        db.execute("""CREATE TABLE patient_sales
        (id INT, patient_id INT
        sales_count INT, PRIMARY KEY(id), FOREIGN KEY(patient_id) REFERENCES patients (id))
        """)
        print("patient sales table created")

    def store_patient_data(self, patients_list, table_name):
        db = self.conn.cursor()
        if table_name == 'patient' or table_name == 'patients':
            for pat in patients_list:
                query = '''INSERT INTO patients (first_name, last_name, address, city, state) VALUES(?, ?, ?, ?, ?, ?)'''
                data = (pat.first_name, pat.last_name, pat.address, pat.city, pat.state)
                db.execute(query, data)
                print(pat.last_name, ": patient info was stored in table")

    def store_patient_sales(self, patients_list, sales_list):
        db = self.conn.cursor()
        for pat in patients:
            db.execute('''INSERT INTO patient_sales (patient_id, sales_count) VALUES (?, ?)''', pat.id, sales_count)

    def save_changes(self):
        self.conn.commit()
        self.conn.close()
