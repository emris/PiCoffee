# encoding: utf-8

from PICoffee import app, db
from flask import render_template, url_for, request, flash
from flask_bootstrap import Bootstrap
from models import Users, CoffeeBrands, CoffeeNames, ActiveData
from forms import LoginForm, RegisterForm, TokensForm, ProfileUpdateForm, CoffeeBrandForm
from werkzeug.utils import redirect
from werkzeug.security import generate_password_hash
from flask_login.utils import login_required, logout_user, login_user, current_user
from sqlalchemy import func

Bootstrap(app)
title="Coffee APP"

@app.route('/')
def index():
  return render_template('index.html', title=title)

@app.route('/login', methods=['GET', 'POST'])
def login():
  form = LoginForm()
  if form.validate_on_submit():
    user = Users.query.filter_by(uid=form.uid.data).first()
    if user.role > 0:
      login_user(user, remember=form.remember.data)
      return redirect(url_for('coffee'))
    flash('User account waiting for approval!', 'info')
  return render_template('login.html', form=form, title=title)

@app.route('/logout')
@login_required
def logout():
  logout_user()
  return render_template('index.html', title=title)

@app.route('/register', methods=['GET', 'POST'])
def register():
  form = RegisterForm()
  if form.validate_on_submit():
      hashpass = generate_password_hash(form.password1.data, method='sha256')
      new = Users(uid=form.uid.data, password=hashpass, email=form.email.data, firstname=form.firstname.data, lastname=form.lastname.data)
      db.session.add(new)
      db.session.commit()
      flash('User '+new.uid+' was Registered and is pending approval.', 'success')
      return redirect('/login')
  return render_template('register.html', form=form, title=title)

@app.route('/coffee')
@login_required
def coffee():
  cu = Users.query.filter_by(id=current_user.id).first()
  return render_template('coffee.html', admin=(cu.role > 1), title=title)

@app.route('/profile')
@login_required
def profile():
  return render_template('profile.html', title=title)

@app.route('/profile/update', methods=['GET', 'POST'])
@login_required
def profile_update():
  form = ProfileUpdateForm()
  cu = Users.query.filter_by(id=current_user.id).first()
  if form.validate_on_submit():
    if form.password1.data != "":
      hashpass = generate_password_hash(form.password1.data, method='sha256')
      cu.password = hashpass
    cu.email = form.email.data
    cu.firstname = form.firstname.data
    cu.lastname = form.lastname.data
    db.session.commit()
    flash('User profile updated.', 'success')
    return redirect(url_for('profile'))
  return render_template('profileupdate.html', form=form, user=cu, title=title)

@app.route('/tokens/<a>', methods=['GET', 'POST'])
@login_required
def tokens(a):
  form = TokensForm()
  cu = Users.query.filter_by(id=current_user.id).first()
  toks=cu.tokens[:]
  if request.method == 'POST':
    if a == "DEL":
      toks.remove(form.token.data)
      cu.tokens = toks
      db.session.commit()
      return redirect('/tokens/list')
    elif form.validate_on_submit():
      toks.append((form.token.data).upper())
      cu.tokens = toks
      db.session.commit()
      return redirect('/tokens/list')
  return render_template('tokens.html', form=form, toks=toks, title=title)

@app.route('/admin/brands/<a>', methods=['GET', 'POST'])
@login_required
def brands(a):
  cu = Users.query.filter_by(id=current_user.id).first()
  if cu.role < 1:
    return redirect('/coffee')

  form = CoffeeBrandForm()
  bmax = db.session.query(CoffeeBrands.name_id, func.max(CoffeeBrands.version).label('vermax')).group_by(CoffeeBrands.name_id).subquery()
  brands = CoffeeBrands.query.join(bmax, bmax.c.vermax == CoffeeBrands.version).filter(bmax.c.name_id == CoffeeBrands.name_id).all()
  adata = ActiveData.query.filter_by(id=1).first()
  if request.method == 'POST':
    if (a == "USE"):
      adata.coffeebrand_id = request.form['id']
      db.session.commit()
      return redirect('/admin/brands/list')
    elif (a == "DEL"):
      brand = CoffeeBrands.query.filter_by(id=request.form['id']).first()
      if brand.hide:
        brand.hide = False
      else:
        brand.hide = True
      db.session.commit()
      return redirect('/admin/brands/list')
    elif (a == "ADD"):
      if form.validate_on_submit():
        cn = CoffeeNames.query.filter_by(name=form.name.data).first()
        if cn:
          brand = CoffeeBrands.query.filter_by(name_id=cn.id).order_by(CoffeeBrands.version.desc()).first()
          cb = CoffeeBrands(cn, form.price.data)
          cb.version = brand.version + 1
          db.session.add(cb)
          db.session.commit()
        else:
          cn = CoffeeNames(form.name.data)
          db.session.add(cn)
          db.session.commit()
          brand = CoffeeBrands(cn, form.price.data)
          db.session.add(brand)
          db.session.commit()
      return redirect('/admin/brands/list')
  if (a == "list"):
    return render_template('brands.html', form=form, brands=brands, brandinuse=adata.coffeebrand_id, title=title)
  return redirect('/coffee')

@app.route('/admin/accounts/<a>', methods=['GET', 'POST'])
@login_required
def accounts(a):
  cu = Users.query.filter_by(id=current_user.id).first()
  if cu.role < 1:
    return redirect('/coffee')

  if request.method == 'POST':
    user = Users.query.filter_by(id=request.form['id']).first()
    if a=="endis":
      if user:
        if (user.role == 0):
          user.role = 1
        else:
          user.role = 0
        db.session.commit()
    if a=="adm":
      if user:
        if (user.role == 2):
          user.role = 1
        else:
          user.role = 2
        db.session.commit()
    return redirect('/admin/accounts/list')

  if (a == "list"):
    users = Users.query.filter(Users.id > 1).all()
    return render_template('accounts.html', users=users, cu=cu, title=title)
  return redirect('/coffee')

@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
  return redirect('/coffee')
