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

        # TODO: Add the user's entry into the database
        first_name = request.form.get("first name")
        last_name = request.form.get("last name")
        birthday = request.form.get("birthday (DD/MM/YYYY)")
        address = request.form.get("address")
        city = request.form.get("city")
        state = request.form.get("state")
        patient = Patient(first_name, last_name, birthday, address, city, state)

        # Set up SQL connection
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
        # Store patient data retrieved into object

        # Display the inputed patient data in the database on index.html
        sales_row = db.execute("SELECT name, sales_count FROM patient_sales")
        print(sales_row)
