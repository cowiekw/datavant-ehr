import sqlite3
import os
from core.patient import Patient
from core.user import User

class SQLPipeline:
    """ A patient class"""
    def __init__(self, name='patients'):
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
        (id INTEGER, first_name TEXT, last_name TEXT, age INT,
         city TEXT, state TEXT, email TEXT, PRIMARY KEY(id))
        """)
        print("patients table created")

        cur.execute("""CREATE TABLE IF NOT EXISTS users
        (id INTEGER, name TEXT, email TEXT)
        """)
        print("users table created")

        cur.execute("""CREATE TABLE IF NOT EXISTS patient_sales
        (id INT, patient_id INT
        sales_count INT, PRIMARY KEY(id), FOREIGN KEY(patient_id) REFERENCES patients (id))
        """)
        print("patient sales table created")

        # Create a table that shows all the hospital sales of user data.
        cur.execute("""CREATE TABLE IF NOT EXISTS research_contributions
        (id INT, user_id INT, project TEXT, seller TEXT, sales_date TIMESTAMP, revenue INT, PRIMARY KEY(id), FOREIGN KEY(user_id) REFERENCES users (id))
        """)
        print("research table created")

    def populate_research_table(self, userid): # After authentication this adds row to research dashboard for each user.
        cur = self.conn.cursor()
        query = '''INSERT INTO research_contributions (user_id, project, seller, sales_date, revenue) VALUES(?, ?, ?, ?, ?)'''
        data = (userid, "COVID-19 research", "University of Farin Medical System", 12/28/2021, "$54.00")
        cur.execute(query, data)
        print(userid, ": user's research table was populated")

    def store_user_data(self, user):
        self.conn.row_factory = sqlite3.Row
        cur = self.conn.cursor()
        query = '''INSERT INTO users (id, name, email) VALUES(?, ?, ?)'''
        data = (user.id, user.name, user.email)
        cur.execute(query, data)
        print(user.name, ": user info was stored in table")

    def store_patient_data(self, pat):
        self.conn.row_factory = sqlite3.Row
        cur = self.conn.cursor()
        query = '''INSERT INTO patients (first_name, last_name, age, city, state, email) VALUES(?, ?, ?, ?, ?, ?)'''
        data = (pat.first_name, pat.last_name, pat.age, pat.city, pat.state, pat.email)
        cur.execute(query, data)
        print(pat.last_name, ": patient info was stored in table")

    def store_patient_sales(self, patients_list, sales_list):
        cur = self.conn.cursor()
        for pat in patients:
            cur.execute('''INSERT INTO patient_sales (patient_id, sales_count) VALUES (?, ?)''', pat.id, sales_count)

    def save_changes(self):
        self.conn.commit()
        self.conn.close()
