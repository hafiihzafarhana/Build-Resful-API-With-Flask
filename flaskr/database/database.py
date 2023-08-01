from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref
from enum import unique
import string
import random

db = SQLAlchemy()


class User(db.Model):  # kelas induk atau kelas dasar
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.Text(), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    bookmark = db.relationship('Bookmark', backref='user')

    def __repr__(self) -> str:
        return 'User>>> {self.username}'


class Bookmark(db.Model):  # kelas induk atau kelas dasar
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, nullable=True)
    url = db.Column(db.Text, nullable=False)
    short_url = db.Column(db.String(3), nullable=True)
    visitor = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def generate_short_characters(self):
        # 0 - 9
        characters = string.digits + string.ascii_letters

        # pick random
        pick_characters = ''.join(random.choices(characters, k=3))

        # check if same with in db
        link = self.query.filter_by(short_url=pick_characters).first()

        if link:
            self.generate_short_characters()
        else:
            return pick_characters

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.short_url = self.generate_short_characters()

    def __repr__(self) -> str:
        return 'Bookmark>>> {self.url}'


'''
catatan:
1)  adanya db.Model, membuat db.Model menjadi kelas dasar atau induk
2) 
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    adanya super() berarti kelas objek akan mengikuti kelas dasar atau induk

3)  Namun, apabila di dalam class tidak ditentukan class induk atau dasarnya, maka akan secara otomatis
    mengikuti class bawaan python yaitu object

4) Jika membuat class, parameter self harus didahulukan
'''
