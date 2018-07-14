# encoding: utf-8

from PICoffee import db, login_manager
from sqlalchemy.dialects.postgresql import ARRAY
from flask_login.mixins import UserMixin

class Users(UserMixin, db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.SmallInteger, primary_key=True)
    uid = db.Column(db.String(5), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(50))
    firstname = db.Column(db.String(50))
    lastname = db.Column(db.String(50))
    tokens = db.Column(ARRAY(db.String(30), dimensions=1), default=[])
    lastlogin = db.Column(db.DateTime, server_onupdate=db.func.now(), nullable=True)
    createtime = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)
    role = db.Column(db.SmallInteger, default=0, nullable=False)
    balance = db.Column(db.Numeric(5, 2), default=0, nullable=False)
    deleted = db.Column(db.Boolean, default=False)
    userconsumption = db.relationship('Consumption', backref='userconsumption', lazy='dynamic')

    def __init__(self, uid, password, email, firstname, lastname):
        self.uid = uid
        self.password = password
        self.email = email
        self.firstname = firstname
        self.lastname = lastname

    def __repr__(self):
        return '<Users %r>' % (self.name)

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

class CoffeeBrands(db.Model):
    __tablename__ = 'CoffeeBrands'
    id = db.Column(db.SmallInteger, primary_key=True)
    name_id = db.Column(db.SmallInteger, db.ForeignKey('CoffeeNames.id'), nullable=False)
    name = db.relationship('CoffeeNames', foreign_keys='CoffeeBrands.name_id', lazy='joined')
    kgprice = db.Column(db.Numeric(5, 2), nullable=False)
    createtime = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)
    hide = db.Column(db.Boolean, default=False)
    version = db.Column(db.SmallInteger, default=0)
    consumptionbrand = db.relationship('Consumption', backref='consumptionbrand', lazy='dynamic')
    activedatabrand = db.relationship('ActiveData', backref='activedatabrand', lazy='dynamic')

    def __init__(self, coffeename, kgprice):
        self.name_id = coffeename.id
        self.kgprice = kgprice

    def __repr__(self):
        return '<CoffeeBrands %r>' % (self.name)

class CoffeeNames(db.Model):
    __tablename__ = 'CoffeeNames'
    id = db.Column(db.SmallInteger, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<CoffeeNames %r>' % (self.name)

class Consumption(db.Model):
    __tablename__ = 'Consumption'
    id =  db.Column(db.SmallInteger, primary_key=True)
    user_id = db.Column(db.SmallInteger, db.ForeignKey('Users.id'), nullable=False)
    coffeebrand_id = db.Column(db.SmallInteger, db.ForeignKey('CoffeeBrands.id'), nullable=False)
    amount = db.Column(db.SmallInteger, default=0)
    time = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)

    def __init__(self, userconsumption, consumptionbrand, amount):
        self.user_id = userconsumption.id
        self.coffeebrand_id = consumptionbrand.id
        self.amount = amount
  
    def __repr__(self):
        return '<Consumption %r>' % (self.name)

class ActiveData(db.Model):
    __tablename__ = 'ActiveData'
    id =  db.Column(db.SmallInteger, primary_key=True)
    coffeebrand_id = db.Column(db.SmallInteger, db.ForeignKey('CoffeeBrands.id'), nullable=False)
    user_id = db.Column(db.SmallInteger, nullable=True)
    inuse = db.Column(db.Boolean, default=False)
    power = db.Column(db.Boolean, default=True)

    def __init__(self, activedatabrand):
        self.coffeebrand_id = activedatabrand.id

    def __repr__(self):
        return '<ActiveData %r>' % (self.name)
