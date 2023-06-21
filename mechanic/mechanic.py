import random

from flask import Blueprint, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

from database import get_session, metadata
from database.models import TerminStanowisko
from database.models import Termin

mechanic_bp = Blueprint('mechanic_bp', __name__,
                        template_folder='templates/mechanic',  static_folder='static')



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