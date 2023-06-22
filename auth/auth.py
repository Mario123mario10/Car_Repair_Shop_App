from sqlalchemy import func
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email
from werkzeug.security import check_password_hash
from database import get_session, metadata, Klient, Uzytkownik
from general import generate_unique_key
from werkzeug.security import generate_password_hash


auth_bp = Blueprint('auth_bp', __name__,
                    template_folder='templates/auth', static_folder='static')

"""
    Tests routes - have to be removed before main released
"""

@auth_bp.route('/data')
def getData():
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
def listOfPersonsAlcheme():
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
    password = PasswordField('Hasło', validators=[DataRequired()])
    role = SelectField('Rola', choices=[('administrator', 'Administrator'), ('mechanik', 'Mechanik'), ('klient', 'Klient')], validators=[DataRequired()])
    submit = SubmitField('Login')


class RegistrationForm(FlaskForm):
    first_name = StringField('Imię', validators=[DataRequired()])
    last_name = StringField('Nazwisko', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone_number = StringField('Numer telefonu', validators=[DataRequired()])
    password = PasswordField('Hasło', validators=[DataRequired()])
    submit = SubmitField('Register')


@auth_bp.route('/', methods=['GET', 'POST'])
def login():
    session = get_session()

    Uzytkownik = metadata.tables['uzytkownik']

    form = LoginForm()
    if form.validate_on_submit():
        user = session.query(Uzytkownik).filter(Uzytkownik.c.adres_mailowy == form.login.data).first()
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
    session = get_session()
    form = RegistrationForm()
    user = None

    if form.validate_on_submit():
        user = Uzytkownik.query.filter_by(adres_mailowy=form.email.data).first()

        if user is None and form.first_name.data:
            new_id = generate_unique_key()
            user = Uzytkownik(id_uz=new_id, imie=form.first_name.data, nazwisko=form.last_name.data, adres_mailowy=form.email.data, skrot_hasla=generate_password_hash(form.password.data), nr_telefonu=form.phone_number.data, typ="klient")
            client = Klient(id_uz=new_id)
            form.first_name.data = ''
            form.last_name.data = ''
            form.password.data = ''
            form.phone_number.data = ''
            form.email.data = ''

            flash('Account created!', 'success')

            session.add(user)
            session.add(client)
            session.commit()
        else:
            flash('Error (maybe this account already exists)!', 'danger')

    session.close()
    return render_template('register.html', form=form)
