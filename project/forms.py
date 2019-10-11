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

class AddPaper(FlaskForm):
    pname=wtforms.StringField('paper name:',validators=[DataRequired(message='input paper name')])
    passm=wtforms.IntegerField('passing percentage',validators=[DataRequired(message='please enter the passing percentage')])
    nm=wtforms.RadioField('negative marking?',choices=[('-1','yes'),('0','no')])
    awm=wtforms.IntegerField('how much marks should 1 question hold?',validators=[DataRequired(message='please enter the marks of on question')])
    submit=wtforms.SubmitField('Add Paper')

class AddQuestion(FlaskForm):
    pid=wtforms.IntegerField(validators=[DataRequired()])
    question=wtforms.TextAreaField(validators=[DataRequired()])
    optionA=wtforms.StringField('OptionA',validators=[DataRequired()])
    optionB=wtforms.StringField('OptionB',validators=[DataRequired()])
    optionC=wtforms.StringField('OptionC',validators=[DataRequired()])
    optionD=wtforms.StringField('OptionD',validators=[DataRequired()])
    rightanswer=wtforms.IntegerField('right option number?',validators=[DataRequired()])
    submit=wtforms.SubmitField('Submit')

class SeeQuestion(FlaskForm):
    pid=wtforms.IntegerField('enter paper id:',validators=[DataRequired()])
    submit=wtforms.SubmitField('see questions')

class DeleteQuestion(FlaskForm):
    qid=wtforms.IntegerField('enter question id:',validators=[DataRequired()])
    submit=wtforms.SubmitField('delete question')

class DeletePaper(FlaskForm):
    pid=wtforms.IntegerField('enter the paper id:',validators=[DataRequired()])
    submit=wtforms.SubmitField('delete paper')

class StudentLogin(FlaskForm):
    sid=wtforms.IntegerField('enter id:',validators=[DataRequired()])
    sname=wtforms.StringField('enter name:',validators=[DataRequired()])
    iid=wtforms.IntegerField('enter institute id:',validators=[DataRequired()])
    submit=wtforms.SubmitField('Log In')

class GiveExam(FlaskForm):
    pid=wtforms.IntegerField('enter paper id:',validators=[DataRequired()])
    submit=wtforms.SubmitField('lets begin the exam')
    
class SeeResult(FlaskForm):
    pid=wtforms.IntegerField('enter paper id:',validators=[DataRequired()])
    submit=wtforms.SubmitField('check result')