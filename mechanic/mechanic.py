from flask import Blueprint, render_template, request, redirect, url_for
from database import get_session, metadata

mechanic_bp = Blueprint('mechanic_bp', __name__,
                    static_folder='static')