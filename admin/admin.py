from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email
from database import get_session, metadata, Klient, Uzytkownik, Mechanik, Administrator, Zlecenie, Pojazd, Status
from general import generate_unique_key
from werkzeug.security import generate_password_hash
from decimal import Decimal
from sqlalchemy import join, func



admin_bp = Blueprint('admin_bp', __name__,
                    template_folder='templates/admin',  static_folder='static')

class RegistrationForm(FlaskForm):
    first_name = StringField('Imię', validators=[DataRequired()])
    last_name = StringField('Nazwisko', validators=[DataRequired()])
    phone_number = StringField('Numer telefonu', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Hasło', validators=[DataRequired()])
    typ = SelectField('Typ', choices=[('klient', 'Klient'), ('mechanik', 'Mechanik'), ('administrator', 'Administrator')],
                      validators=[DataRequired()])
    pensja = StringField('Pensja')
    submit = SubmitField('Register')


class ZlecenieForm(FlaskForm):
    description_before_repair = StringField('Opis przed naprawą', validators=[DataRequired()])
    date_of_admission = StringField('Data przyhęcia', validators=[DataRequired()])
    estimated_repair_time = StringField('Szacowany czas naprawy', validators=[DataRequired()])
    vehicle_id = StringField('ID pojazdu', validators=[DataRequired()])
    mechanik_id = StringField('ID mechanika', validators=[DataRequired()])


@admin_bp.route('/')
def admin_dashboard():
    return render_template('admin_main.html')


@admin_bp.route('/orders', methods=['GET', 'POST'])
def show_orders():
    session = get_session()
    if request.method == 'POST':
        # Handle form submission if needed
        pass

    # Perform a join query to fetch the necessary information from related models
    query = session.query(
        Zlecenie.opis_przed_naprawa,
        Zlecenie.data_przyjecia,
        Zlecenie.szacowany_czas_naprawy,
        Status.opis.label('status_zlecenia'),
        Pojazd.marka,
        Pojazd.model,
        Pojazd.rok_produkcji,
        Uzytkownik.imie,
        Uzytkownik.nazwisko
    ).join(
        Status, Zlecenie.status_id_stat == Status.id_stat
    ).join(
        Pojazd, Zlecenie.pojazd_id_poj == Pojazd.id_poj
    ).join(
        Mechanik, Zlecenie.mechanik_id_uz == Mechanik.id_uz
    ).join(
        Uzytkownik, Mechanik.id_uz == Uzytkownik.id_uz
    )

    # Execute the query and fetch the results
    results = query.all()

    # Create a list of dictionaries with the fetched data
    orders = [
        {
            'opis_przed_naprawa': order.opis_przed_naprawa,
            'data_przyjecia': order.data_przyjecia,
            'szacowany_czas_naprawy': order.szacowany_czas_naprawy,
            'status_zlecenia': order.status_zlecenia,
            'pojazd': f"{order.marka} {order.model} {order.rok_produkcji}",
            'mechanik': f"{order.imie} {order.nazwisko}"
        }
        for order in results
    ]

    session.close()
    return render_template('orders.html', orders=orders)


@admin_bp.route('/orders/addOrder', methods=['GET', 'POST'])
def addOrder():
    session = get_session()
    form = ZlecenieForm()
    zlecenie = None
    status = None

    print("I am here")

    if form.validate_on_submit():
        new_zlecenie_id = generate_unique_key()
        new_status_id = generate_unique_key()
        status = Status(id_stat=new_status_id, opis="backlog")
        session.add(status)

        zlecenie = Zlecenie(
            id_zlec=new_zlecenie_id,
            opis_przed_naprawa=form.description_before_repair.data,
            data_przyjecia=form.date_of_admission.data,
            szacowany_czas_naprawy=form.estimated_repair_time.data,
            pojazd_id_poj=form.vehicle_id.data,
            mechanik_id_uz=form.mechanik_id.data,
            status_id_stat=new_status_id
        )
        session.add(zlecenie)

        form.description_before_repair.data = ''
        form.date_of_admission.data = ''
        form.estimated_repair_time.data = ''
        form.vehicle_id.data = ''
        form.mechanik_id.data = ''

        session.commit()
        session.close()

        return redirect(url_for('admin_bp.show_orders'))

    session.close()
    return render_template('add_order.html', form=form)



@admin_bp.route('/register', methods=['GET', 'POST'])
def create_account():
    session = get_session()
    form = RegistrationForm()
    user = None

    if form.validate_on_submit():
        user = Uzytkownik.query.filter_by(adres_mailowy=form.email.data).first()

        if user is None and form.first_name.data:
            new_id = generate_unique_key()
            user = Uzytkownik(id_uz=new_id, imie=form.first_name.data, nazwisko=form.last_name.data, adres_mailowy=form.email.data, skrot_hasla=generate_password_hash(form.password.data), nr_telefonu=form.phone_number.data, typ=form.typ.data)
            session.add(user)

            if form.typ.data == "klient":
                client = Klient(id_uz=new_id)
                session.add(client)
            elif form.typ.data == "mechanik" and form.pensja.data is not None:
                pensjaN = Decimal(form.pensja.data)
                mechanic = Mechanik(id_uz=new_id, pensja=pensjaN)
                session.add(mechanic)
            elif form.typ.data == "administrator":
                admin = Administrator(id_uz=new_id)
                session.add(admin)
            else:
                flash('Missing one of the field!', 'danger')


            form.first_name.data = ''
            form.last_name.data = ''
            form.password.data = ''
            form.phone_number.data = ''
            form.email.data = ''
            form.typ.data = ''
            form.pensja.data = ''

            flash('Account created!', 'success')

            
            session.commit()
        else:
            flash('Error (maybe this account already exists)!', 'danger')

    session.close()
    return render_template('registration.html', form=form)


@admin_bp.route('/complaints')
def show_complaints():
    session = get_session()
    reklamacja = metadata.tables['reklamacja']
    rozwiazanie = metadata.tables['rozwiazanie']
    zreal_napr = metadata.tables['zrealnapr']

    query = session.query(
        reklamacja.c.opis.label("Opis reklamacji"),
        rozwiazanie.c.nazwa.label("Co nalezy zrobic"),
        zreal_napr.c.data_realizacji.label("Data naprawy"),
        zreal_napr.c.opis_po_naprawie.label("Opis naprawy")
    ).join(
        rozwiazanie, rozwiazanie.c.id_rozw == reklamacja.c.rozwiazanie_id_rozw
    ).join(
        zreal_napr, zreal_napr.c.id_napr == reklamacja.c.zrealnapr_id_napr
    )
    results = query.all()
    # Convert the results to a list of dictionaries
    data = [dict(row) for row in results]

    session.close()

    return render_template('complaints.html', data=data)
