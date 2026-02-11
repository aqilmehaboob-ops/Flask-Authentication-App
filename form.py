from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SubmitField
from wtforms.validators import DataRequired

class Form(FlaskForm):
    name = StringField(label="Name", validators=[DataRequired()])
    password = PasswordField(label="Password", validators=[DataRequired()])
    age = IntegerField(label="Age", validators=[DataRequired()])
    submit = SubmitField(label="Submit")
