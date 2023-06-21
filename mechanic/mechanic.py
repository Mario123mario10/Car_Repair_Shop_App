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
    return render_template('mechanic_main.html')
    return render_template('mechanic_main.html')

class RegistrationForm(FlaskForm):

    ID_stanowiska = StringField('Stanowisko ID', validators=[DataRequired()])
    ID_zlecenia = StringField('Zlecenie ID', validators=[DataRequired()])
    submit = SubmitField('Register')


@mechanic_bp.route('/registerforplace', methods=['GET', 'POST'])
def registerforplace():
    session = get_session()
    form = RegistrationForm()
    if request.method == 'POST':
        id_stan_r = request.form['ID_stanowiska']
        id_zlecenie_r = request.form['ID_zlecenia']
        termin_czas_rozpoczecia_r = request.form['Czas rozpoczecia']
        termin_czas_zakonczenia_r = request.form['Czas zakonczenia']
        id_mechanika_r = request.form['id_mechanika']
        typ_r = "stanowisko"  
        if not (id_stan_r and id_zlecenie_r):
            error_message = 'Not all required fields are completed.'
            return render_template('admin.html', error_message=error_message)
        id_wpisu_v = random.randint(0,100)
        termin = Termin(id_wpisu = id_wpisu_v, czas_rozpoczecia = termin_czas_rozpoczecia_r, czas_zakonczenia=termin_czas_zakonczenia_r, mechanik_id_uz=id_mechanika_r, typ=typ_r)
        registration_for_place = TerminStanowisko(id_wpisu=id_wpisu_v, stanowisko_id_stan = int(id_stan_r), zlecenie_id_zlec = int(id_zlecenie_r))
        session.add(termin)
        session.add(registration_for_place)
        session.commit()
    session.close()
    return render_template('register_for_place.html', form=form)
