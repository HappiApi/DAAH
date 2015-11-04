from app import db
from sqlalchemy.dialects.postgresql import JSON

from passlib.hash import sha256_crypt

#OLD USER CLASS
"""
class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String())
    password = db.Column(db.String())

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return '<User %r>' % (self.username)
"""
class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), index=True, unique=True)
    password = db.Column('password', db.String(128))

    def __init__(self, password=None):
        self.password = password

    def get_password(self):
        return self.password

    def set_password(self, password):
        if password:
            self.password = sha256_crypt.encrypt(password, rounds=12345)

    def password_checking(self, password):
        if self.password is None:
            return False
        return sha256_crypt.verify(password, self.password)

    def check_password(self, password):
        authenticated = self.password_checking(password) if user else False

        return authenticated

    def __repr__(self):
        return '<User %r>' % (self.username)

    def get_id(self):
        return str(self.username)


class List(db.Model):
    __tablename__ = 'list'

    id = db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, name, user_id):
        self.name = name
        self.user_id = user_id

    def __repr__(self):
        return '<List %r>' % (self.name)

class Task(db.Model):
    __tablename__ = 'task'

    id = db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String())
    list_id = db.Column(db.Integer, db.ForeignKey('list.id'))

    def __init__(self, name, list):
        self.name = name
        self.list_id = list.id

    def __repr__(self):
        return '<Task %r>' % (self.name)
