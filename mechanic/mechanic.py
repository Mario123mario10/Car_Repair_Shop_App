from flask import Blueprint, render_template, request, redirect, url_for
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
