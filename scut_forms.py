from flask_wtf import FlaskForm, validators
from wtforms import StringField, BooleanField, DateTimeField, TextAreaField, IntegerField, SubmitField, DateField, \
    PasswordField
from wtforms.validators import DataRequired, Length, NumberRange

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password')
    submit = SubmitField('Submit')

class RegistrationForm(FlaskForm):
    username     = StringField('Username', validators=[Length(1, 64)])
    email        = StringField('Email Address', validators=[Length(6, 36)])
    accept_rules = BooleanField('I accept the site rules', validators=[DataRequired()])

class ProfileForm(FlaskForm):
    birthday  = DateField('Your Birthday', format='%Y-%m-%d')
    signature = TextAreaField('Forum Signature')

class AdminProfileForm(ProfileForm):
    username = StringField('Username', validators=[Length(max =40)])
    level    = IntegerField('User Level', validators=[NumberRange(min=0, max=10)])
    submit = SubmitField('Submit')
