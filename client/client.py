from flask import Blueprint, render_template, request, redirect, url_for
from database import get_session, metadata

client_bp = Blueprint('client_bp', __name__,
                    static_folder='static')