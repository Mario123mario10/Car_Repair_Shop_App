from sqlalchemy import func
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email
from werkzeug.security import check_password_hash
from database import get_session, metadata
# from ..client import client_bp
# from ..mechanic import admin_bp
# from ..admin import mechanic_bp


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
class LoginForm(FlaskForm):
    login = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    role = SelectField('Role', choices=[('administrator', 'Administrator'), ('mechanik', 'Mechanik'), ('klient', 'Klient')], validators=[DataRequired()])
    submit = SubmitField('Login')

@auth_bp.route('/', methods=['GET', 'POST'])
def login():
    session = get_session()

    Uzytkownik = metadata.tables['uzytkownik']
    Klient = metadata.tables['klient']
    Mechanik = metadata.tables['mechanik']
    Admin = metadata.tables['administrator']

    form = LoginForm()
    if form.validate_on_submit():
        user = session.query(Uzytkownik).filter(Uzytkownik.c.adres_mailowy == form.login.data).first()
        print(user)
        if user:
            if check_password_hash(user.skrot_hasla, form.password.data):
                role = form.role.data
                if role == 'administrator' and user.typ == 'administrator':
                    return redirect(url_for('admin_bp.admin_dashboard'))
                elif role == 'mechanik' and user.typ == 'mechanik':
                    return redirect(url_for('mechanic_bp.mechanic_dashboard'))
                elif role == 'klient' and user.typ == 'klient':
                    return redirect(url_for('client_bp.client_dashboard'))
                else:
                    flash('Invalid role selected for this user', 'danger')
            else:
                flash('Invalid password', 'danger')
        else:
            flash('Invalid email', 'danger')

    session.close()

    return render_template('auth.html', form=form)



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
        return render_template('mechanic/mechanic_main.html')
    elif role == 'administrator':
        return render_template('admin/admin_main.html')
    else:
        return render_template('client/client_main.html')
