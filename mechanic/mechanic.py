from random import random

from flask import Blueprint, render_template, request, redirect, url_for
from database import get_session, metadata

mechanic_bp = Blueprint('mechanic_bp', __name__,
                        template_folder='templates/mechanic',  static_folder='static')


@mechanic_bp.route('/')
def mechanic_dashboard():
    return render_template('mechanic_main.html')


@mechanic_bp.route('/registerforplace', methods=['GET', 'POST'])

def registerforplace():

    if request.method == 'POST':

        # Get form data

        terminstanowisko = metadata.tables['terminstanowisko']

        id_stan = request.form['ID_stanowiska']

        id_zlecenie = request.form['ID_zlecenia']




        # Perform validation

        if not (

                id_stan and id_zlecenie):

            error_message = 'Not all required fields are completed.'

            return render_template('admin.html', error_message=error_message)




        # Register the user as a client

        task = {

            'id_wpisu': random.randint(0,10),

            'stanowisko_id_stan': id_stan,

            'zlecenie_id_zlec': id_zlecenie

        }

        terminstanowisko.append(task)




        return redirect(url_for('login'))

    return render_template('register_for_place.html')@mechanic_bp.route('/registerforplace', methods=['GET', 'POST'])

def registerforplace():

    if request.method == 'POST':

        # Get form data

        terminstanowisko = metadata.tables['terminstanowisko']

        id_stan = request.form['ID_stanowiska']

        id_zlecenie = request.form['ID_zlecenia']




        # Perform validation

        if not (

                id_stan and id_zlecenie):

            error_message = 'Not all required fields are completed.'

            return render_template('admin.html', error_message=error_message)




        # Register the user as a client

        task = {

            'id_wpisu': random.randint(0,10),

            'stanowisko_id_stan': id_stan,

            'zlecenie_id_zlec': id_zlecenie

        }

        terminstanowisko.append(task)
        return redirect(url_for('login'))

    return render_template('register_for_place.html')