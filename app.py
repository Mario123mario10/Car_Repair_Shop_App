from flask import Flask
from auth import auth_bp
from client import client_bp
from admin import admin_bp
from mechanic import mechanic_bp
from database import configure_database

def create_app():
    app = Flask(__name__)
    configure_database(app)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(client_bp, url_prefix='/client')
    app.register_blueprint(mechanic_bp, url_prefix='/mechanic')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    return app
    

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
