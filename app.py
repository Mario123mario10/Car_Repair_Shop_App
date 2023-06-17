from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv('.env')
USER_NAME = os.environ.get("USER_NAME")
PASSWORD = os.environ.get("PASSWORD")
HOSTNAME = os.environ.get("HOSTNAME")
PORT = os.environ.get("PORT")
SERVICE_NAME = os.environ.get("SERVICE_NAME")

# Create the Flask application
app = Flask(__name__)

# Configure the Oracle database connection string
db_uri = f'oracle+cx_oracle://{USER_NAME}:{PASSWORD}@{HOSTNAME}:{PORT}/?service_name={SERVICE_NAME}'
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

# Create the SQLAlchemy database object
db = SQLAlchemy(app)

# Create the database engine for direct connection
engine = create_engine(db_uri)

# Reflect the existing Oracle database tables
metadata = db.MetaData(bind=engine)
metadata.reflect()

# Access the reflected tables
Table1 = metadata.tables['klient']

@app.route('/')
def index():
    return 'Hello, World!'

@app.route('/data')
def get_data():
    # Perform a query on the reflected tables
    with engine.connect() as conn:
        result = conn.execute(Table1.select())
        data = result.fetchall()
    return str(data)

if __name__ == '__main__':
    app.run(debug=True)
