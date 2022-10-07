from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    email = db.Column(db.String, primary_key=True, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)


db.create_all()

archie = User(email="archie.andrews@email.com", password="football4life")
veronica = User(email="veronica.lodge@email.com", password="fashiondiva")

db.session.add(archie)
db.session.add(veronica)

try:
    db.session.commit()
except Exception as e:
    db.session.rollback()
finally:
    db.session.close()
