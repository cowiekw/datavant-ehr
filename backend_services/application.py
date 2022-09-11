import sqlite3
from flask import Flask, flash,  url_for, jsonify, redirect, render_template, request, session
from authlib.integrations.flask_client import OAuth
import os
from werkzeug.exceptions import abort
from datetime import timedelta
from core.store_sql import SQLPipeline
from core.patient import Patient
from auth_decorator import login_required # decorator for routes that should be accessible only by logged in users

# dotenv setup
from dotenv import load_dotenv
load_dotenv()

# Configure application
app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True  # Ensure templates are auto-reloaded

app.secret_key = os.getenv("APP_SECRET_KEY")
app.config['SESSION_COOKIE_NAME'] = 'google-login-session'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=15)


#oauth config
def fetch_token(name, request):
    token = OAuth2Token.find(
        name=name,
        user=request.user
    )
    return token.to_token()

oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=os.getenv("GOOGLE_CLIENT_ID"), # from google Developer account
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',  # This is only needed if using openId to fetch user info
    # server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid profile email'}, # Scope is what Google returns
    fetch_token=fetch_token,
    jwks_uri="https://www.googleapis.com/oauth2/v3/certs"
)

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

@app.route("/")
def index():
    email = dict(session).get('email', None) # Return none if there's no email
    return render_template("index.html", email=email)

@app.route('/login')
def login():
    google = oauth.create_client('google')
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/authorize')
def authorize():
    google = oauth.create_client('google')
    token = google.authorize_access_token()
    resp = google.get('userinfo',token=token) # User info contains name, email, picture profil
    user_info = resp.json()
    user = oauth.google.userinfo()  # uses openid endpoint to fetch user info
    # resp.raise_for_status()
    # do something with the token and profile
    session['email']=user_info['email']
    session['profile'] = user_info
    session.permanent = True  # make the session permanant so it keeps existing after broweser gets closed
    return redirect('/')

@app.route('/logout')
def logout():
    for key in list(session.keys()):
        session.pop(key) # Remove each key in the session
    return redirect('/') # redirect home

@app.route("/account", methods=["GET", "POST"])
def account():
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

        return render_template("account.html")
        sqlcon.save_changes() # Close the connection

@app.route("/mydata", methods=["GET", "POST"])
@login_required # decorate that redirects user to login.
def mydata(patient_rows=None):
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

        return render_template("mydata.html", patient_rows=patient_rows)
        sqlcon.save_changes() # Close the connection


@app.route("/about", methods=["GET", "POST"])

def about():
    if request.method == "POST":
        return render_template("about.html")

    elif request.method == "GET":
        return render_template("about.html")
