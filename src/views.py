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

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
  form = LoginForm()
  if form.validate_on_submit():
    user = Users.query.filter_by(uid=form.uid.data).first()
    if user.role > 0:
      login_user(user, remember=form.remember.data)
      return redirect(url_for('coffee'))
    flash('User account waiting for approval!', 'info')
  return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
  logout_user()
  return render_template('index.html')

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
  return render_template('register.html', form=form)

@app.route('/coffee')
@login_required
def coffee():
  user = Users.query.filter_by(id=current_user.id).first()
  if user.role > 1:
    return render_template('coffee.html', admin=True)
  return render_template('coffee.html', admin=False)

@app.route('/profile')
@login_required
def profile():
  return render_template('profile.html')

@app.route('/profile/update', methods=['GET', 'POST'])
@login_required
def profile_update():
  form = ProfileUpdateForm()
  user = Users.query.filter_by(id=current_user.id).first()
  if form.validate_on_submit():
    if form.password1.data != "":
      hashpass = generate_password_hash(form.password1.data, method='sha256')
      user.password = hashpass
    user.email = form.email.data
    user.firstname = form.firstname.data
    user.lastname = form.lastname.data
    db.session.commit()
    flash('User profile updated.', 'success')
    return redirect(url_for('profile'))
  return render_template('profileupdate.html', form=form, user=user)

@app.route('/tokens/<a>', methods=['GET', 'POST'])
@login_required
def tokens(a):
  form = TokensForm()
  user = Users.query.filter_by(id=current_user.id).first()
  toks=user.tokens[:]
  if request.method == 'POST':
    if a == "DEL":
      toks.remove(form.token.data)
      user.tokens = toks
      db.session.commit()
      return redirect('/tokens/list')
    elif form.validate_on_submit():
      toks.append((form.token.data).upper())
      user.tokens = toks
      db.session.commit()
      return redirect('/tokens/list')
  return render_template('tokens.html', form=form, toks=toks)

@app.route('/admin/brands/<a>', methods=['GET', 'POST'])
@login_required
def brands(a):
  au = Users.query.filter_by(id=current_user.id).first()
  if au.role < 1:
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
      return render_template('brands.html', form=form, brands=brands, brandinuse=adata.coffeebrand_id)
  if (a == "list"):
    return render_template('brands.html', form=form, brands=brands, brandinuse=adata.coffeebrand_id)
  return redirect('/coffee')

@app.route('/admin/accounts/<a>', methods=['GET', 'POST'])
@login_required
def accounts(a):
  au = Users.query.filter_by(id=current_user.id).first()
  if au.role < 1:
    return redirect('/coffee')

  if request.method == 'POST':
    user = Users.query.filter_by(id=request.form['id']).first()
    if user:
      if (user.role == 0):
        user.role = 1
      else:
        user.role = 0
      db.session.commit()
    return redirect('/admin/accounts/list')

  if (a == "list"):
    users = Users.query.filter(Users.id > 1).all()
    return render_template('accounts.html', users=users)
  return redirect('/coffee')

@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
  return redirect('/coffee')
