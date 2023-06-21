from flask import Blueprint, render_template, request, redirect, url_for
from sqlalchemy import text
from database import get_session, metadata
from flask import flash

mechanic_bp = Blueprint('mechanic_bp', __name__,
                        template_folder='templates/mechanic',  static_folder='static')

# Define your SQL queries
sql_queries = {
    'table1': "SELECT marka AS \"Marka pojazdu\", model AS \"Model Pojazdu\", rok_produkcji AS \"Rok produkcji pojazdu\" FROM pojazd",
    'table2': "SELECT id_masz AS \"Numer maszyny\", koszt AS \"Koszt maszyny\", data_zakupu AS \"data zakupu\", opis_stanu as \"stan maszyny\" FROM maszyna",
    'table3': "SELECT marka AS \"Marka pojazdu\", model AS \"Model Pojazdu\", rok_produkcji AS \"Rok produkcji pojazdu\" FROM pojazd",
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