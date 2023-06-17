from flask import Blueprint, render_template, request, redirect, url_for
from database import get_session, metadata

admin_bp = Blueprint('admin_bp', __name__,
                    static_folder='static')