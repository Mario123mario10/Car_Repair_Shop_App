from flask import Blueprint, render_template, request, redirect, url_for
from database import get_session, metadata

mechanic_bp = Blueprint('mechanic_bp', __name__,
                        template_folder='templates/mechanic',  static_folder='static')


@mechanic_bp.route('/')
def mechanic_dashboard():
    return render_template('mechanic_main.html')