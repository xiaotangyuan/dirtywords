import os
import json
import datetime
import flask_login
from flask_sqlalchemy import SQLAlchemy
from main import db


class Member(flask_login.UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    openid = db.Column(db.String(120), unique=True, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    created_date = db.Column(db.DateTime, nullable=False)

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<Member %r>' % self.email

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False


class WordLib(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.String(120), nullable=False)
    wordlibname = db.Column(db.String(120), nullable=False)
    wordjsonlist = db.Column(db.Text, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    created_date = db.Column(db.DateTime, nullable=False)

    def get_words_list(self):
        words = json.loads(self.wordjsonlist)
        if self.wordlibname in ['wordlib1', 'wordlib2']:
            return words
        words_list = []
        for w_line in words:
            words_list += w_line.split('；')
        return words_list

