from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
database_name = "trivia"
database_path = "postgresql://postgres:postgres@{}/{}".format('localhost:5432', database_name)

app.config["SQLALCHEMY_DATABASE_URI"] = database_path
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)



