import random

from flask import Blueprint, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

from database import get_session, metadata
from database.models import Reklamacja, Rozwiazanie

client_bp = Blueprint('client_bp', __name__,
                    template_folder='templates/client',  static_folder='static')


class ComplaintForm(FlaskForm):

    ID_fix = StringField('ID naprawy', validators=[DataRequired()])
    description_fix = StringField('Zlecenie ID', validators=[DataRequired()])
    expected_solution = StringField('Zlecenie ID', validators=[DataRequired()])
    submit = SubmitField('Register')


@client_bp.route('/')
def client_dashboard():
    return render_template('client_main.html')



@client_bp.route('/makeacomplaint')
def client_dashboard():
    def registerforplace():
        session = get_session()
        form = ComplaintForm()
        if request.method == 'POST':
            id_fix= request.form['ID_fix']
            description = request.form['description_fix']
            expected_solution = request.form['expected_solution']
            
            if not (description and id_fix and expected_solution):
                error_message = 'Not all required fields are completed.'
                return render_template('admin.html', error_message=error_message)
            id_entry = random.randint(0, 100)
            rozwiazanie = Rozwiazanie(id_rozw = id_entry, nazwa = expected_solution)
            reklamacja = Reklamacja(id_rekl=id_entry, opis = description, rozwiazanie_id_rozw=id_entry,zrealnapr_id_napr=id_fix)
        
            session.add(reklamacja)
            session.commit()
        session.close()
        return render_template('make_a_complaint.html', form=form)