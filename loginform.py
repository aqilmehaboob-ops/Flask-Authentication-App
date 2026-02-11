from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    name = StringField(label="name", validators=[DataRequired()])
    password = PasswordField(label="password", validators=[DataRequired()])
    submit = SubmitField(label="submit")