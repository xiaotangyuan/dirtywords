import hashlib
import os
import datetime
from main import app
from flask_sqlalchemy import SQLAlchemy

filepath = os.path.dirname(os.path.abspath(__file__))
dbfile = os.path.join(filepath, 'dirtywords.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////%s' % dbfile
# print(dbfile)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    openid = db.Column(db.String(120), unique=True, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    created_date = db.Column(db.DateTime, nullable=False)


class WordLib(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.String(120), nullable=False)
    wordlibname = db.Column(db.String(120), nullable=False)
    wordjsonlist = db.Column(db.Text, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

