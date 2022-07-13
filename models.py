#encoding: utf-8
from exts import db
from datetime import datetime

class Boss(db.Model):
    __tablename__ = 'boss'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    signal = db.Column(db.String(100), nullable=False)


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    create_time = db.Column(db.DateTime, default=datetime.now)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), nullable=False)

class Tenement(db.Model):
    __tablename__ = 'tenement'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    create_time = db.Column(db.DateTime, default=datetime.now)
    flat_name = db.Column(db.String(50),nullable=False)
    flat_id = db.Column(db.String(50))
    room_count = db.Column(db.Integer,nullable=False)
    bathroom_count = db.Column(db.Integer,nullable=False)
    kitchen_count = db.Column(db.Integer)
    livingroom_count = db.Column(db.Integer)
    price = db.Column(db.String(50),nullable=False)
    deposit = db.Column(db.Integer,nullable=False)
    telephone1 = db.Column(db.String(50),nullable=False)
    telephone2 = db.Column(db.String(50))
    address = db.Column(db.String(100),nullable=False)
    kitchen = db.Column(db.String(50),nullable=False)
    window = db.Column(db.String(50), nullable=False)
    lift = db.Column(db.String(50), nullable=False)
    remark = db.Column(db.String(1000))
    hasMoveIn = db.Column(db.Boolean, nullable=False)
    image1 = db.Column(db.String(200))
    image2 = db.Column(db.String(200))
    image3 = db.Column(db.String(200))
    image4 = db.Column(db.String(200))
    image5 = db.Column(db.String(200))
    image6 = db.Column(db.String(200))


class Recruit(db.Model):
    __tablename__ = 'recruit'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    create_time = db.Column(db.DateTime, default=datetime.now)
    unit = db.Column(db.String(100), nullable=True)
    content = db.Column(db.String(100), nullable=True)
    category = db.Column(db.String(100), nullable=True)
    pay = db.Column(db.String(100), nullable=True)
    commend = db.Column(db.String(100))
    address = db.Column(db.String(100), nullable=True)
    contact = db.Column(db.String(100), nullable=True)
    remark = db.Column(db.String(1000))
    hasMoveIn = db.Column(db.Boolean, nullable=False)