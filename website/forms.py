from random import choices
from secrets import choice
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,DateField,DateTimeField,FileField, TextAreaField,SelectField,BooleanField,IntegerField, SubmitField
from wtforms.validators import DataRequired,Email
from flask_wtf.file import FileField, FileAllowed, FileRequired
#choices
Year=['First Year','Second Year','Third Year','Fourth Year']
Dept=['Arch','CE','ECE','EE','EG','ICE','IT']



class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[Email()])
    role = SelectField('Role', validators=[DataRequired()])
    year = SelectField('Year' ,validators=[DataRequired()])
    dept = SelectField('Department', validators=[DataRequired()])
    submit = SubmitField('Submit')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class BlogForm(FlaskForm):
    upload = FileField('Blog Image', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png'], 'Images only!')
    ])
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content')
    author = StringField('Author', validators=[DataRequired()])
    submit = SubmitField('Create Blog')


class GroundForm(FlaskForm):
    groundName = StringField('Ground Name', validators=[DataRequired()])
    NoOfCourt = IntegerField('No Of Court', validators=[DataRequired()])
    bookTime = StringField('Book Time', validators=[DataRequired()])
    submit = SubmitField('Submit')


class BookingForm(FlaskForm):
    groundName = StringField('Ground Name', validators=[DataRequired()])
    courtName = StringField('Court Name', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()])
    time = SelectField('Time' ,validators=[DataRequired()])
    submit = SubmitField('Submit')