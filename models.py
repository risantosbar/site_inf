from flask_login import UserMixin
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError, EqualTo, Email, DataRequired
from app import db
from string import ascii_letters, digits, ascii_lowercase, ascii_uppercase
 
 
class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(40), nullable=False, unique=True)
    password = db.Column(db.String(20), nullable=False)
 
 
def validate_username(self, username):
        existing_user_username = Users.query.filter_by(
            username=username.data).first()
        allowed = ascii_letters + '_' + digits
        if existing_user_username:
            raise ValidationError('Этот логин уже существует.')
        if not (username.data[0] in ascii_letters):
            raise ValidationError('Логин может начинаться только с символа латинского алфавита.')
        if not all(i in allowed for i in username.data):
            raise ValidationError('Логин может содержать только символы латинского алфавита, цифры и знак _.')
       
def validate_email(self, email):
    existing_user_email = Users.query.filter_by(
        email=email.data).first()
    if existing_user_email:
        raise ValidationError('Уже существует пользователь с таким адресом электронной почты.')
 
def validate_password(self, password):
    validated = True
    symbols = '.,;:!?%$#@&*^|\~[]{/}'
    if not any(i in ascii_lowercase for i in password.data): validated = False
    if not any(i in ascii_uppercase for i in password.data): validated = False
    if not any(i in digits for i in password.data): validated = False
    if not any(i in symbols for i in password.data): validated = False
    if not validated:
        raise ValidationError('''Пароль должен содержать по крайней мере одну цифру, букву в каждом регистре
        и один из следующих символов: .,;:!?%$#@&*^|\~[]{/}.''')
 
 
class RegisterForm(FlaskForm):
   
    username = StringField(validators=[
        InputRequired(), Length(min=6, max=20), validate_username], render_kw={
            "placeholder": "Логин", "class": "form-control"})
 
    email = StringField(validators=[
        DataRequired(), Length(min=6, max=40), Email(), validate_email], render_kw={
            "placeholder": "Е-mail", "class": "form-control"})
 
    password = PasswordField(validators=[
        InputRequired(), Length(min=8, max=20), validate_password], render_kw={"placeholder": "Пароль", "class": "form-control"})
   
    confirm  = PasswordField('Подтвердите пароль', [
        InputRequired(), EqualTo('password', message='Пароли не совпадают!')], render_kw={
            "placeholder": "Подтвердите пароль", "class": "form-control"})
 
    submit = SubmitField('Зарегистрироваться', render_kw={"class":"btn btn-primary"})
 
class LoginForm(FlaskForm):
    username = StringField(validators=[
        InputRequired(), Length(min=6, max=20)], render_kw={"placeholder": "Логин", "class": "form-control"})
 
    password = PasswordField(validators=[
        InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Пароль", "class": "form-control"})
 
    submit = SubmitField('Войти', render_kw={"class":"btn btn-primary"})
