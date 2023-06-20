from flask import Blueprint, render_template, request, redirect, url_for
from database import get_session, metadata

admin_bp = Blueprint('admin_bp', __name__,
                    template_folder='templates/admin',  static_folder='static')


@admin_bp.route('/')
def admin_dashboard():
    return render_template('admin_main.html')