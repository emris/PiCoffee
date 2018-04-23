# encoding: utf-8

from PICoffee import db
from models import Users, CoffeeNames, CoffeeBrands, ActiveData

#Create DB
db.create_all()

# Add Admin User (Pass: ChangeMe ) and a few test Tokens
u = Users("admin", "sha256$wKLjUqT1$d39c19c386b69d8051d55f645ce9abf75e8ea4ed897207b1c2dd23553967a4ee", "admin@test.org", "Admin", "Admin")
u.tokens = ["12345678", "11223344"]
u.role = 3
u.registered = True
db.session.add(u)
db.session.commit()

# Add a few Coffee Brands
cn = CoffeeNames("Roen Extra Bar")
db.session.add(cn)
db.session.commit()
c = CoffeeBrands(cn, 16.68)
db.session.add(c)
db.session.commit()

cn = CoffeeNames("Red Honey Coffee")
db.session.add(cn)
db.session.commit()
c = CoffeeBrands(cn, 23.99)
db.session.add(c)
db.session.commit()

cn = CoffeeNames("Nordish.Coffee")
db.session.add(cn)
db.session.commit()
c = CoffeeBrands(cn, 28.90)
db.session.add(c)
db.session.commit()

# Config default Coffee brand
a = ActiveData(activedatabrand=c)
db.session.add(a)
db.session.commit()
