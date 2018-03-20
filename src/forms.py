# encoding: utf-8

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from werkzeug.security import check_password_hash
from models import Users

class LoginForm(FlaskForm):
  uid = StringField('UserID', validators=[InputRequired(), Length(min=4, max=5)])
  password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
  remember = BooleanField('Remember')
  
  def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)
        self.user = None
  
  def validate(self):
    rv = FlaskForm.validate(self)
    if not rv:
      return False
    
    user = Users.query.filter_by(uid=self.uid.data).first()
    if not user:
      self.uid.errors.append('Not found!')
      return False
    
    if not check_password_hash(user.password, self.password.data):
      self.password.errors.append('Vertippt?!')
      return False
    
    return True

class RegisterForm(FlaskForm):
  uid = StringField('UserID', validators=[InputRequired(), Length(min=4, max=5)])
  password1 = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
  password2 = PasswordField('Password Echo', validators=[InputRequired(), Length(min=8, max=80)])
  email = StringField('E-Mail', validators=[InputRequired(), Email(message='Invalid E-Mail'), Length(max=60)])
  firstname = StringField('First Name', validators=[InputRequired(), Length(min=4, max=20)])
  lastname = StringField('Last Name', validators=[InputRequired(), Length(min=4, max=20)])
  
  def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)
        self.user = None
  
  def validate(self):
    rv = FlaskForm.validate(self)
    if not rv:
      return False
    
    user = Users.query.filter_by(uid=self.uid.data).first()
    if user:
      self.uid.errors.append('Wurde schon geopfert!')
      return False
    
    if (self.password1.data != self.password2.data):
      self.password2.errors.append('Vertippt!')
      return False
    
    return True

class TokensForm(FlaskForm):
  token = StringField('New Token', validators=[InputRequired(), Length(min=8, max=14)])
  
  def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)
  
  def validate(self):
    rv = FlaskForm.validate(self)
    if not rv:
      return False

    try:
      int(self.token.data, 16)
    except ValueError:
      self.token.errors.append('Token Invalid!'.decode('utf-8'))
      return False
    
    return True

class ProfileUpdateForm(FlaskForm):
  password1 = PasswordField('Password', validators=[Length(max=80)])
  password2 = PasswordField('Password Echo', validators=[Length(max=80)])
  email = StringField('E-Mail', validators=[InputRequired(), Email(message='Invalid E-Mail'), Length(max=60)])
  firstname = StringField('First Name', validators=[InputRequired(), Length(min=4, max=20)])
  lastname = StringField('Last Name', validators=[InputRequired(), Length(min=4, max=20)])
  
  def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)
  
  def validate(self):
    rv = FlaskForm.validate(self)
    if not rv:
      return False
    
    if (self.password1.data != self.password2.data):
      self.password2.errors.append('Vertippt!')
      return False
    
    return True
