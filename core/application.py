import sqlite3
from flask import Flask, flash, jsonify, redirect, render_template, request, session
import psycopg2
from psycopg2 import Error
import pandas as pd

from core.sql_db import SQLPipeline
from core.patient import Patient

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.route("/", methods=["GET", "POST"])
def index():
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
        sqlcon.store_data(patients, 'patient')

        except Exception as ex:
                print("Exception:", ex)
        finally:
            SQLCon.save_changes()

        return redirect("/")

    else:
        # Deliver patient name and EHR sales count

        # Display the inputed patient data in the database on index.html
        patients_row= db.execute("SELECT first_name, last_name, id FROM patients")
        sales = db.execute('''SELECT sales_count from patient_sales WHERE patient_id = id FROM patient_sales VALUES(?)''', patient_id)
        print(name, sales_row) #

        return render_template("index.html", patients = patients_row)
