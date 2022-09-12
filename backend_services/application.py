import sqlite3
from flask import Flask, flash,  url_for, jsonify, redirect, render_template, request, session
from authlib.integrations.flask_client import OAuth
import os
from werkzeug.exceptions import abort
from datetime import timedelta
from core.store_sql import SQLPipeline
from core.patient import Patient
from core.user import User
from auth_decorator import login_required # decorator for routes that should be accessible only by logged in users
import stripe

# dotenv setup
from dotenv import load_dotenv
load_dotenv()

# Configure application
app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True  # Ensure templates are auto-reloaded
app.secret_key = os.getenv("APP_SECRET_KEY")
app.config['SESSION_COOKIE_NAME'] = 'google-login-session'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=15)

stripe_keys = {
    "secret_key": os.environ["STRIPE_SECRET_KEY"],
    "publishable_key": os.environ["STRIPE_PUBLISHABLE_KEY"],
}
stripe.api_key = stripe_keys["secret_key"]

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
    return render_template("index.html")

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
    print(user_info)
    with open('user.txt', 'w') as f:
        f.write('userinfo')
    user = oauth.google.userinfo()  # uses openid endpoint to fetch user info
    # resp.raise_for_status()
    # do something with the token and profile
    session['id'], session['name'],session['email'] =user_info['id'], user_info['name'], user_info['email']
    session['profile'] = user_info
    session.permanent = True  # make the session permanant so it keeps existing after broweser gets closed
    user = User(session['id'], session['name'], session['email']) # Store authenticated user object

    # Set up SQL connection and Store user information
    sqlcon = get_db_conn()
    sqlcon.store_user_data(user) # insert user object into the users table.
    sqlcon.populate_research_table(session['id'])
    sqlcon.save_changes() # Close the connection
    return redirect('/')

@app.route('/logout')
def logout():
    for key in list(session.keys()):
        session.pop(key) # Remove each key in the session
    return redirect('/') # redirect home

@app.route("/join", methods=["GET", "POST"])
@login_required
def join(): # TO DO: change this page, so it's a sign up for sharing public data.
    email = dict(session).get('email', None)
    if request.method == "POST":
        # ADD USER: Add the user's entry into the database
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        age = request.form.get("age")
        city = request.form.get("city")
        state = request.form.get("state")
        patient = Patient(first_name, last_name, age, city, state, session['email'])
        print("patient obj: ", patient)
    # Set up SQL connection and Store patient identifier information
        sqlcon = get_db_conn()
        print("JOIN post connection created")
        sqlcon.store_patient_data(patient) # insert patient object into the patients table.
        sqlcon.save_changes() # Close the connection
        return redirect("/directory")

    elif request.method == "GET":

        # sqlcon = get_db_conn()
        # print("get connection created")
        # cur = sqlcon.conn.cursor()
        # cur.execute("SELECT first_name, last_name, age city, state, email FROM patients")
        # patient_rows = cur.fetchall()
        # print("row:", patient_rows)
        # sqlcon.save_changes() # Close the connection
        return render_template("join.html")

# Create a directory to view data that is being share with researchers
@app.route("/directory")
@login_required # decorate that redirects user to login.
def directory():
    patient_rows=[]
    # Display the entries in the directory based on data submitted on the Join page.
    sqlcon = get_db_conn()
    print("directory get connection created")
    cur = sqlcon.conn.cursor()
    cur.execute("SELECT first_name, last_name, age, state, email FROM patients")
    patient_rows = cur.fetchall()
    sqlcon.save_changes() # Close the connection
    print("row:", patient_rows)
    # sales = cur.execute('''SELECT sales_count from patient_sales WHERE patient_id = id FROM patient_sales VALUES(?)''', patient_id)
    return render_template("directory.html", patient_rows=patient_rows)


# Create a dashboard to view Sales of your health data
@app.route("/dashboard", methods=["GET"])
@login_required
def dashboard():
    sales_row =[]
    sqlcon = get_db_conn()
    cur = sqlcon.conn.cursor()
    cur.execute('''SELECT project, seller, sales_date, revenue FROM research_contrubitions WHERE user_id = VALUES(?)''', session['user_id'])
    sales_rows = cur.fetchall()
    return render_template("dashboard.html", sales_rows=sales_rows)
    sqlcon.save_changes() # Close the connection

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/payment")
@login_required
def payment():
    return render_template("payment.html")

@app.route('/charge', methods=['POST'])
def charge():
    # Amount in cents
    amount = 1.00
    customer = stripe.Customer.create(
        email='customer@example.com',
        source=request.form['stripeToken']
    )

    charge = stripe.Charge.create(
        customer=customer.id,
        amount=amount,
        currency='usd',
        description='Flask Charge'
    )

    return render_template('charge.html', amount=amount)
