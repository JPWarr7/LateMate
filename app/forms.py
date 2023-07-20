from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, TextAreaField, DateField, RadioField, BooleanField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, StopValidation, NumberRange, EqualTo
from wtforms.widgets import CheckboxInput, ListWidget
from enum import Enum

# class RequestStatus(Enum):
#     Pending = 1
#     Approved = 2
#     Denied = 3
#     Returned = 4
#     Final_Approval = 5

# Login form (subclassed from FlaskForm)
class SignInForm(FlaskForm):
    email = StringField('Email: ', validators=[DataRequired()])
    password = PasswordField('Password: ', validators=[DataRequired()])
    submit = SubmitField('Sign In')

class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Current Password:', validators=[DataRequired()])
    new_password = PasswordField('New Password:', validators=[DataRequired()])
    confirm_new_password = PasswordField('Confirm New Password:', validators=[DataRequired(), EqualTo('new_password', message='Passwords must match.')])
    submit = SubmitField('Change Password:')
    
class SignUpForm(FlaskForm):
    first_name = StringField('First Name:', validators=[DataRequired()])
    last_name = StringField('Last Name:', validators=[DataRequired()])    
    email = StringField('Email:', validators=[DataRequired()])
    student_id = StringField('student_id:', validators=[DataRequired()])
    password = PasswordField('Password:', validators=[DataRequired()])
    passwordRetype = PasswordField('Confirm Password: ', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Sign up')
    
class LateAddForm(FlaskForm):
    date = DateField('Request Date: ', validators =[DataRequired()], format='%Y-%m-%d')
    term = SelectField('Term: ', choices=[('Spring 2023'),('Summer 2023'),('Fall 2023'),('Winter 2023')])
    student_id = IntegerField('Student ID', validators=[DataRequired(), NumberRange(min=1, max=99999999, message="Please enter a valid student ID")])
    email = StringField('Email:', validators=[DataRequired()])
    course_id = IntegerField('Course ID: ',validators=[DataRequired()])
    comments = StringField('Comments (Optional): ')
    submit = SubmitField('Forward Request')
    
class DropForm(FlaskForm):
    date = DateField('Request Date: ', validators =[DataRequired()], format='%Y-%m-%d')
    term = SelectField('Term: ', choices=[('Spring 2023'),('Summer 2023'),('Fall 2023'),('Winter 2023')])
    student_id = IntegerField('Student ID', validators=[DataRequired(), NumberRange(min=1, max=99999999, message="Please enter a valid student ID")])
    email = StringField('Email:', validators=[DataRequired()])
    course_id = IntegerField('Course ID: ',validators=[DataRequired()]) # <- possible add in future sprint, course association with user to check if they're taking it or not. 
    comments = StringField('Comments (Optional): ')
    submit = SubmitField('Forward Request')
    
class CourseForm(FlaskForm):
    date = DateField('Request Date: ', validators =[DataRequired()], format='%Y-%m-%d')
    term = SelectField('Term: ', choices=[('Spring 2023'),('Summer 2023'),('Fall 2023'),('Winter 2023')])
    student_id = IntegerField('Student ID', validators=[DataRequired(), NumberRange(min=1, max=99999999, message="Please enter a valid student ID")])
    email = StringField('Email:', validators=[DataRequired()])
    course_id = IntegerField('Course ID: ',validators=[DataRequired()])
    comments = StringField('Comments (Optional): ')
    submit = SubmitField('Forward Request')

class ApproverForm(FlaskForm):
    action = SelectField('Term: ', choices=[('Add'),('Remove')])
    name = StringField ('Name: ', validators = [DataRequired()])
    approver_id = IntegerField('Approver ID: ', validators=[DataRequired(), NumberRange(min=1, max=99999999, message="Please enter a valid student ID")])
    email = StringField('Approver Email: ', validators=[DataRequired()])
    comments = StringField('Comments (Optional): ')
    submit = SubmitField('Update')

class FilterForm(FlaskForm):
    filt = SelectField('Filter By: ', choices=[('Name'),('Student ID'),('Course'),('Term')])
    filterInput = StringField('Type:', validators=[DataRequired()])
    submit = SubmitField('Filter')

class ViewRequestForm(FlaskForm):
    # request_status = SelectField('Status', coerce=int, validators=[DataRequired()])
    comments = TextAreaField('Comments', validators=[DataRequired()])
    approve = SubmitField('Approve')
    deny = SubmitField('Deny')

    # def __init__(self, *args, **kwargs):
    #     super(ViewRequestForm, self).__init__(*args, **kwargs)
    #     self.request_status.choices = [(s.value, s.name) for s in RequestStatus]
        
class ReportsForm(FlaskForm):
    gen = SelectField('Generate: ', choices=[('Name'),('Student ID'),('Course'),('Term')])
    GenInput = StringField('Type:', validators=[DataRequired()])
    submit = SubmitField('Generate Report')
    deny = SubmitField('deny')
