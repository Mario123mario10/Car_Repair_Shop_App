from flask import Blueprint, render_template, request, redirect, url_for
from database import get_session, metadata

client_bp = Blueprint('client_bp', __name__,
                    template_folder='templates/client',  static_folder='static')


@client_bp.route('/')
def client_dashboard():
    return render_template('client_main.html')