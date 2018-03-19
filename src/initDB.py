# encoding: utf-8

from PICoffee import app, db
from models import Users, CoffeeBrands, ActiveData

#Create DB
db.create_all()

# Add Admin User with Password "1234qwer" and a few test Tokens
u = Users("admin", "sha256$XCRgZK7p$0177c009969b8e1aee62e97b25d52c091117c82266cbfc565447ce74882b9f72", "admin@test.org", "Admin", "Admin")
u.tokens = ["12345678", "11223344"]
u.role = 2
u.registered = True
db.session.add(u)
db.session.commit()

# Add a few Coffee brands 
c = CoffeeBrands("Happy Coffee", 25.90, db.func.current_timestamp(), False)
db.session.add(c)
c = CoffeeBrands("Red Honey Coffee", 23.99, db.func.current_timestamp(), False)
db.session.add(c)
c = CoffeeBrands("Nordish.Coffee", 28.90, db.func.current_timestamp(), False)
db.session.add(c)
db.session.commit()

# Config default Coffee brand
a = ActiveData(activedatabrand=c)
db.session.add(a)
db.session.commit()
