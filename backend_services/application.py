import sqlite3
from flask import Flask, flash, jsonify, redirect, render_template, request, session
import pandas as pd

from core.store_sql import SQLPipeline
from core.patient import Patient

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.route("/", methods=["GET", "POST"])
def index(patient_rows=None):
    patients_row='fake_patient'
    if request.method == "POST":

        # ADD USER: Add the user's entry into the database
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        birthday = request.form.get("birthday")
        address = request.form.get("address")
        city = request.form.get("city")
        state = request.form.get("state")

        patient = Patient(first_name, last_name, birthday, address, city, state)
        print("patient obj: ", patient)
        # Set up SQL connection and Store patient identifier information
        sqlcon = SQLPipeline()
        try:
            sqlcon.create_connection()
            sqlcon.create_table()
            cur = sqlcon.conn.cursor()
            print("cursor made")
            sqlcon.store_patient_data(patient, 'patients') # insert patient object into the patients table.
            sqlcon.save_changes() # Close the connection
        except Exception as ex:
                print("Exception:", ex)
        return redirect("/")

    elif request.method == "GET":
     # DISPLAY USER INFO: Display the entries in the database on index.html
        try:
            sqlcon = SQLPipeline()
            sqlcon.create_connection()
            sqlcon.create_table()
            print("get connection created")
            cur = sqlcon.conn.cursor()
            print("get curr created")
            cur.execute("SELECT first_name, last_name, birthday, address, city, state FROM patients")
            patient_rows = cur.fetchall()
            print("row:", patient_rows)
            # sales = cur.execute('''SELECT sales_count from patient_sales WHERE patient_id = id FROM patient_sales VALUES(?)''', patient_id)

            return render_template("index.html", patient_rows=patient_rows)
            sqlcon.save_changes() # Close the connection

        except Exception as ex:
            print("Exception:", ex)
