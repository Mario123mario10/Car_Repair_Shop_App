from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, MetaData
from dotenv import load_dotenv
import os

load_dotenv('.env')

db = SQLAlchemy()
engine = None
metadata = MetaData()

def configure_database(app):
    global engine, metadata
    # Configure the Oracle database connection string
    db_uri = get_db_uri()
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    db.init_app(app)
    engine = create_engine(db_uri)
    metadata.reflect(bind=engine)

def get_db_uri():
    USER_NAME = os.environ.get("USER_NAME")
    PASSWORD = os.environ.get("PASSWORD")
    HOSTNAME = os.environ.get("HOSTNAME")
    PORT = os.environ.get("PORT")
    SERVICE_NAME = os.environ.get("SERVICE_NAME")
    return f'oracle+cx_oracle://{USER_NAME}:{PASSWORD}@{HOSTNAME}:{PORT}/?service_name={SERVICE_NAME}'

def get_session():
    session = db.create_scoped_session(options={"bind": engine})
    return session
