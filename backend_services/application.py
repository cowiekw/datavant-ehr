import sqlite3
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from werkzeug.exceptions import abort
from core.store_sql import SQLPipeline
from core.patient import Patient

def get_db_conn():
    sqlcon = SQLPipeline()
    try:
        sqlcon.create_connection()
        sqlcon.create_table()
        print("cursor made")
        return sqlcon
    except Exception as ex:
            print("Exception:", ex)

def get_patient(patient_id):
    conn = get_db_connection()
    patient_record = conn.execute('SELECT * FROM patients WHERE id = ?',
                            (patient_id)).fetchone() # Get a single patient record
    conn.close()
    if patient is None:
        abort(404)
    return patient_record

def get_sales_count(patient_record):  # Find the sales count for the patient
    conn = get_db_connection()
    sales_count = conn.execute('SELECT * FROM patient_sales WHERE patient_id = ?',
                            (patient_record.id)).fetchone()
    return sales_count

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        return redirect("/")
    elif request.method == "GET":
        return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
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
        sqlcon = get_db_conn()
        sqlcon.store_patient_data(patient, 'patients') # insert patient object into the patients table.
        sqlcon.save_changes() # Close the connection
        return redirect("/account")

    elif request.method == "GET":
     # DISPLAY USER INFO: Display the entries in the database on account.html

        sqlcon = get_db_conn()
        print("get connection created")
        cur = sqlcon.conn.cursor()
        cur.execute("SELECT first_name, last_name, birthday, address, city, state FROM patients")
        patient_rows = cur.fetchall()
        print("row:", patient_rows)
        # sales = cur.execute('''SELECT sales_count from patient_sales WHERE patient_id = id FROM patient_sales VALUES(?)''', patient_id)

        return render_template("register.html")
        sqlcon.save_changes() # Close the connection


@app.route("/account", methods=["GET", "POST"])
def account(patient_rows=None):
    patients_row='fake_patient'
    if request.method == "POST":
        return redirect("/account")

    elif request.method == "GET":
     # DISPLAY USER INFO: Display the entries in the database on account.html

        sqlcon = get_db_conn()
        print("get connection created")
        cur = sqlcon.conn.cursor()
        cur.execute("SELECT first_name, last_name, birthday, address, city, state FROM patients")
        patient_rows = cur.fetchall()
        print("row:", patient_rows)
        # sales = cur.execute('''SELECT sales_count from patient_sales WHERE patient_id = id FROM patient_sales VALUES(?)''', patient_id)

        return render_template("account.html", patient_rows=patient_rows)
        sqlcon.save_changes() # Close the connection


@app.route("/about", methods=["GET", "POST"])

def about():
    if request.method == "POST":
        return render_template("about.html")

    elif request.method == "GET":
        return render_template("about.html")
