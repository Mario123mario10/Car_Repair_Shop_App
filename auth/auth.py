from sqlalchemy import func
from flask import Blueprint, render_template, request, redirect, url_for
from database import get_session, metadata

auth_bp = Blueprint('auth_bp', __name__,
                    template_folder='templates/auth', static_folder='static')

"""
    Tests routes - have to be removed before main released
"""

@auth_bp.route('/data')
def get_data():
    session = get_session()
    Klient = metadata.tables['klient']
    data = session.query(Klient.c.id_uz).all()
    session.close()
    
    return str(data)


@auth_bp.route('/listOfCarsSql', methods=['GET'])
def listOfCars():
    session = get_session()
    reportTitle = "CarssListSql"
    sqlQuery = "SELECT marka AS \"Marka pojazdu\", model AS \"Model Pojazdu\", rok_produkcji AS \"Rok produkcji pojazdu\" FROM pojazd"

    results = session.execute(sqlQuery)

    # Convert the results to a list of dictionaries
    data = [dict(row) for row in results]

    session.close()

    return render_template('report.html', reportTitle=reportTitle, data=data)


@auth_bp.route('/listOfCarsSqlAlcheme', methods=['GET'])
def listOfPersons_alcheme():
    session = get_session()
    Pojazd = metadata.tables['pojazd']
    reportTitle = "CarsListSqlAlcheme"

    results = session.query(Pojazd.c.marka.label("Marka pojazdu"), Pojazd.c.model.label("Model Pojazdu"), Pojazd.c.rok_produkcji.label("Rok produkcji pojazdu")).all()

    # Convert the results to a list of dictionaries
    data = [dict(row) for row in results]

    session.close()

    return render_template('report.html', reportTitle=reportTitle, data=data)


"""
    Actual code
"""
# In-memory user database for demonstration purposes
users = [
    {'username': 'mechanic1', 'password': 'mechpass1', 'role': 'mechanic'},
    {'username': 'admin1', 'password': 'adminpass1', 'role': 'administrator'},
    {'username': 'client1', 'password': 'clientpass1', 'role': 'client'}
]

@auth_bp.route('/', methods=['GET', 'POST'])
def login():
    error_flag = False

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
        if authenticate_user(username, password, role):
            return redirect(url_for('dashboard', role = role)) 
        else:
            error_message = 'Invalid credentials. Please try again.'
            error_flag = True
            return render_template('auth.html', error = error_flag, error_message=error_message)
    return render_template('auth.html')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get form data
        street = request.form['street']
        house_number = request.form['house_number']
        apartment_number = request.form['apartment_number']
        zip_code = request.form['zip_code']
        city = request.form['city']
        country = request.form['country']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        phone_number = request.form['phone_number']
        email = request.form['email']
        password = request.form['password']
        
        # Perform validation
        if not (street and house_number and zip_code and city and country and first_name and last_name and phone_number and email and password):
            error_message = 'Not all required fields are completed.'
            return render_template('register.html', error_message=error_message)

        # Register the user as a client
        user = {
            'username': email,
            'password': password,
            'role': 'client'
        }
        users.append(user)

        return redirect(url_for('login'))

    return render_template('register.html')


@auth_bp.route('/dashboard/<role>')
def dashboard(role):
    # Replace this logic with your own implementation to retrieve the currently logged-in user
    if role== 'mechanic':
        return render_template('mechanic/mechanic_dashboard.html')
    elif role == 'administrator':
        return render_template('admin/admin_dashboard.html')
    else:
        return render_template('client/client_dashboard.html')


def authenticate_user(username, password, role):
    for user in users:
        if user['username'] == username and user['password'] == password and user['role'] == role:
            return True
    return False
