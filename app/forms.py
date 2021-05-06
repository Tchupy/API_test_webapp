from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    # loginForm class inherits from FlaskForm class
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    cahuete = StringField('Cahuete_label')
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class TokenForm(FlaskForm):
    # loginForm class inherits from FlaskForm class
    token = StringField('Meraki Token', validators=[DataRequired()])
    submit = SubmitField('Validate')