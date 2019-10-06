import wtforms
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms.fields.html5 import EmailField
class AdminSignup(FlaskForm):
    admin_name=wtforms.StringField('Name:',validators=[DataRequired(message='input you name')])
    email_id=EmailField('Email',validators=[DataRequired(message='input a valid email')])
    institute=wtforms.StringField('Institute:',validators=[DataRequired(message='please enter the university')])
    password=wtforms.PasswordField('Password:',validators=[DataRequired(message='please enter the password')])
    rpassword=wtforms.PasswordField('Re-type password:',validators=[DataRequired(message='please retype the password')])
    signup=wtforms.SubmitField('sign up!')

class AdminLogin(FlaskForm):
    email_id=EmailField('Email',validators=[DataRequired(message='input a valid email')])
    password=wtforms.PasswordField('Password:',validators=[DataRequired(message='please enter the password')])
    login=wtforms.SubmitField('Login')

class AddStudent(FlaskForm):
    name=wtforms.StringField('Student name:',validators=[DataRequired(message='input student name')])
    submit=wtforms.SubmitField('Add Student')

class DeleteStudent(FlaskForm):
    id=wtforms.IntegerField('enter student id:',validators=[DataRequired(message='input student id')])
    submit=wtforms.SubmitField('Delete student')