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
def index():
    patients_row=[]
    if request.method == "POST":

        # Add the user's entry into the database
        first_name = request.form.get("first name")
        last_name = request.form.get("last name")
        birthday = request.form.get("birthday (DD/MM/YYYY)")
        address = request.form.get("address")
        city = request.form.get("city")
        state = request.form.get("state")

        patient = Patient(first_name, last_name, birthday, address, city, state)

        # Set up SQL connection and Store patient identifier information
        sqlcon = SQLPipeline()
        try:
            sqlcon.create_connection()
            sqlcon.create_table()
            db = sqlcon.conn.cursor()
            sqlcon.store_patient_data(patient, 'patients') # insert patietn objective from form into patients table.
        except Exception as ex:
                print("Exception:", ex)
        finally:
            sqlcon.save_changes()
        return render_template("index.html", patients = patients_row)
    else:  # GET
        patients = ['fake patient']
        try:
            sqlcon = SQLPipeline()
            sqlcon.create_connection()
            sqlcon.create_table()
            db = sqlcon.conn.cursor()
            patients_row=db.execute("SELECT first_name, last_name, id FROM patients")
            # sales = db.execute('''SELECT sales_count from patient_sales WHERE patient_id = id FROM patient_sales VALUES(?)''', patient_id)

        except Exception as ex:
                print("Exception:", ex)
        return render_template("index.html", patients = patients_row)

        sqlcon.save_changes()
