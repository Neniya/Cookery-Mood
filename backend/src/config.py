import os
SECRET_KEY = os.urandom(32)
SQLALCHEMY_TRACK_MODIFICATIONS = False
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database

db_username = "postgres"
db_password = "postgres123"
db_host = "localhost:5432"
db_name = "easylist"


SQLALCHEMY_DATABASE_URI = 'postgresql://{}:{}@{}/{}'.format(
                db_username, db_password, db_host, db_name 
                )


