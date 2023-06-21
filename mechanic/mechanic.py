import random

from flask import Blueprint, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

from database import get_session, metadata
from database.models import TerminStanowisko
from database.models import Termin
from sqlalchemy import text
from database import get_session, metadata
from flask import flash

mechanic_bp = Blueprint('mechanic_bp', __name__,
                        template_folder='templates/mechanic',  static_folder='static')

# Define your SQL queries
sql_queries = {
    'table1': "SELECT marka AS \"Marka pojazdu\", model AS \"Model Pojazdu\", rok_produkcji AS \"Rok produkcji pojazdu\" FROM pojazd",
    'zlecenie': "SELECT id_zlec AS \"Numer Zlecenia\", opis_przed_naprawa AS \"Opis przed naprawą\", data_przyjecia AS \"Data przyjęcia\", szacowany_czas_naprawy AS \"Szacowany czas naprawy\", pojazd_id_poj AS \"ID Pojazdu\", status_id_stat AS \"ID Statusu\", mechanik_id_uż AS \"ID Mechanika\" FROM zlecenie WHERE mechanik_id_uż = 4",
    'table2': "SELECT id_masz AS \"Numer maszyny\", koszt AS \"Koszt maszyny\", data_zakupu AS \"data zakupu\", opis_stanu as \"stan maszyny\" FROM maszyna",
    'table3': "SELECT id_mag \"Id magazynu\", nazwa AS \"Nazwa magazynu\", pojemnosc_m3 AS \"Pojemnosc\" FROM magazyn",
    'reservation': "SELECT r.nazwa AS \"Nazwa części\", SUM(p.liczba_sztuk) AS \"Liczba sztuk\" FROM pozmag p JOIN rodzajczesci r ON p.rodzajczesci_id_czesci = r.id_czesci WHERE p.magazyn_id_mag = :condition_value GROUP BY r.nazwa"

}


@mechanic_bp.route('/')
def mechanic_dashboard():
    session = get_session()
    machines = metadata.tables['maszyna']
    reservations= metadata.tables['terminmaszyna']
    dates= metadata.tables['termin']
    reportTitle = "Lista rezerwacji maszyn"

    query = session.query(
        dates.c.czas_rozpoczecia.label("Czas rozpoczecia rezerwacji"),
        dates.c.czas_zakonczenia.label("Czas zakonczenia rezerwcji"),
        machines.c.nazwa.label("Nazwa maszyny")
    ).join(
        machines, machines.c.id_masz == reservations.c.maszyna_id_masz
    ).join(
        dates, dates.c.id_wpisu == reservations.c.id_wpisu
    )
    results = query.all()
    # Convert the results to a list of dictionaries
    data = [dict(row) for row in results]

    session.close()

    return render_template('mechanic_main.html')

@mechanic_bp.route('/registerstats')
def register_stats():

    return render_template('register_stats.html')
class RegistrationForm(FlaskForm):

    ID_stanowiska = StringField('Stanowisko ID', validators=[DataRequired()])
    ID_zlecenia = StringField('Zlecenie ID', validators=[DataRequired()])
    submit = SubmitField('Register')




@mechanic_bp.route('/registerforplace', methods=['GET', 'POST'])
def registerforplace():
    session = get_session()
    form = RegistrationForm()
    if request.method == 'POST':
        id_stan = request.form['ID_stanowiska']
        id_zlecenie = request.form['ID_zlecenia']
        termin_czas_rozpoczecia = request.form['Czas rozpoczecia']
        termin_czas_zakonczenia = request.form['Czas zakonczenia']
        id_mechanika = request.form['id_mechanika']
        typ = "Stanowisko"
        if not (id_stan and id_zlecenie):
            error_message = 'Not all required fields are completed.'
            return render_template('admin.html', error_message=error_message)
        id_wpisu = random.randint(0,100)
        termin = Termin(id_wpisu=id_wpisu,czas_rozpoczecia=termin_czas_rozpoczecia, czas_zakonczenia=termin_czas_zakonczenia, mechanik_id_uz=id_mechanika, typ=typ)
        registration_for_place = TerminStanowisko(id_wpisu = id_wpisu, stanowisko_id_stan = int(id_stan), zlecenie_id_zlec = int(id_zlecenie))
        session.add(termin)
        session.add(registration_for_place)
        session.commit()
    session.close()
    return render_template('register_for_place.html', form=form)
@mechanic_bp.route('/<table_id>')
def mechanic_dashboard(table_id=None):
    data = None
    if table_id:
        session = get_session()
        sql_query = text(sql_queries.get(table_id))
        result_proxy = session.execute(sql_query)
        keys = result_proxy.keys()
        data = [dict(zip(keys, row)) for row in result_proxy]
        session.close()
    return render_template('mechanic_main.html', table_id=table_id, data=data)


@mechanic_bp.route('/print/<message>')
def print_message(message):
    # session = get_session()
    # sql_query = text("UPDATE table_name SET column_name = :message WHERE condition_column = :condition_value")
    # session.execute(sql_query, {'message': message, 'condition_value': condition_value})
    # session.commit()
    # session.close()
    flash('Book complited!', 'success')
    print(message)
    return redirect(url_for('mechanic_bp.mechanic_dashboard'))

@mechanic_bp.route('/reserve/<message>')
def reserve(message):
    session = get_session()
    sql_query = text(sql_queries.get('reservation'))
    print(message)
    result_proxy = session.execute(sql_query, {'condition_value': message})
    keys = result_proxy.keys()
    data = [dict(zip(keys, row)) for row in result_proxy]
    session.close()
    #flash('Reservation successful!', 'success')
    return render_template('mechanic_main.html', table_id='reservation', data=data)

@mechanic_bp.route('/zlecenie/<message>')
def zlecenie(message):
    session = get_session()
    sql_query = text(sql_queries.get('zlecenie'))
    print(message)
    message = 4
    result_proxy = session.execute(sql_query, {'condition_value': message})
    keys = result_proxy.keys()
    data = [dict(zip(keys, row)) for row in result_proxy]
    session.close()
    return render_template('mechanic_main.html', table_id='zlecenie', data=data)
