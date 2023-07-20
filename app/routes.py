from app import app
from flask import render_template, redirect, send_from_directory, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.forms import LateAddForm, DropForm, SignUpForm, SignInForm, ChangePasswordForm, FilterForm, ViewRequestForm, ReportsForm, ApproverForm, CourseForm 
from app import db
from app.models import *
import sys
from flask import abort
from datetime import datetime
from enum import Enum
from flask_mail import Mail, Message

# mail send
mail = Mail(app)

def send_mail(addr, msg):
    recipient = addr
    message = msg
    subject = 'Test Flask email'
    msg = Message(subject, recipients=[recipient], body = message)
    mail.send(msg)

def request_created(student, crn, type):
    course = Course.query.filter_by(crn=crn).first()
    approver = Approver.query.filter_by(id=course.professor_id).first()
    prof_msg = f"Hello {approver.title}, {student.first_name} {student.last_name} has submitted a{type} request for {course.subject} {course.course}-{course.section}."
    student_msg = f"Hello {student.first_name} {student.last_name}, your {type} request for {course.subject} {course.course}-{course.section} has been sent to {approver.title}."
    return prof_msg, student_msg

def status_change(student, crn):
    course = Course.query.filter_by(crn=crn).first()
    approver = Approver.query.filter_by(id=course.professor_id).first()
    student_msg = f"Hello {student.first_name} {student.last_name}, your request for {course.subject} {course.course}-{course.section} has been reviewed and the status has changed."
    return student_msg

@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)


@app.route('/')
def index():
    return render_template('landing.html')

@app.route('/login', methods = ['GET', 'POST'])
def signin():
    form = SignInForm()
    if form.validate_on_submit():
        user = db.session.query(User).filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            print(f'Login failed for user: {user.first_name} {user.last_name}', file=sys.stderr)
            print(f'Provided email: {form.email.data}', file=sys.stderr)
            print(f'Provided password: {form.password.data}', file=sys.stderr)
            print(f'User object: {user}', file=sys.stderr)
            return redirect(url_for('signin'))

        login_user(user)
        print('Login successful', file=sys.stderr)
        if user.role == 'student':
            return redirect(url_for('studentHome'))
        else:
            return redirect(url_for('approverHome'))
    return render_template('signin.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        # Read data from form fields
        first_name = form.first_name.data
        last_name = form.last_name.data
        student_id = form.student_id.data
        email = form.email.data
        password = form.password.data
      
        # Create new user object and add to database
        user = User( first_name=first_name, last_name=last_name, student_id=student_id, email=email, role = 'student')
        user.set_password(password)
        
        student = Student(first_name=first_name, last_name=last_name, student_id=student_id, email=email, role='student', major="Example Major", gpa=3.5)
        student.set_password(password)
        db.session.add(student)
        
        db.session.commit()

        return redirect(url_for('signin'))
    
    # Render signup form template
    return render_template('signup.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('signin'))

@app.route('/changepassword', methods=['GET', 'POST'])
@login_required
def changepassword():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        user = current_user
        if not check_password_hash(user.password, form.current_password.data):
            flash('Incorrect current password.', 'danger')
        else:
            new_password_hash = generate_password_hash(form.new_password.data)
            user.password = new_password_hash
            db.session.commit()
            flash('Your password has been updated. Please sign in again.', 'success')
            logout_user()  # Add this line to log the user out after changing the password
            return redirect(url_for('signin'))
    return render_template('changepassword.html', form=form)


@app.route('/student')
@login_required
def student():
    # Add logic for the student view here
    return render_template('student.html')

@app.route('/lateadd', methods=['GET', 'POST'])
@login_required
def lateadd():
    form = CourseForm()
    if form.validate_on_submit():
        student = Student.query.filter_by(id=current_user.id).first()
        course = Course.query.filter_by(crn=form.course_id.data).first()
        add_request = Request(date=form.date.data,
                         term=form.term.data,
                         student_id=student.id,
                         email=student.email,
                         course_id=course.crn,
                         comments=form.comments.data,
                         approver_id=1, status_id=1,
                         type = "Late Add")
        # Assign an approver
        approver = Approver.query.filter_by(id=course.professor_id).first() 
        if not approver:
            flash('No approvers found. Please contact the admin.', 'danger')
            return redirect(url_for('lateadd'))
        
        add_request.approver_id = approver.id

        db.session.add(add_request)
        db.session.commit()
        prof_msg, student_msg = request_created(student, course.crn, "n add")
        subject = 'Late Add Request'
        msg = Message(subject, recipients=[approver.email ], body = prof_msg)
        msg2 = Message(subject, recipients=[student.email], body = student_msg)
        mail.send(msg)
        mail.send(msg2)
        flash('Your late add request has been submitted', 'success')
        return redirect(url_for('lateadd'))
    return render_template('lateadd.html', title='Late Add Request', form=form)

@app.route('/latedrop', methods=['GET', 'POST'])
@login_required
def latedrop():
    form = CourseForm()
    if form.validate_on_submit():
        student = Student.query.filter_by(id=current_user.id).first()
        course = Course.query.filter_by(crn=form.course_id.data).first()
        drop_request = Request(date=form.date.data,
                         term=form.term.data,
                         student_id=student.id,
                         email=student.email,
                         course_id=form.course_id.data,
                         comments=form.comments.data,
                         approver_id=1, status_id=1,
                         type = "Drop")
        # Assign an approver
        approver = Approver.query.filter_by(id=course.professor_id).first() 
        if not approver:
            flash('No approvers found. Please contact the admin.', 'danger')
            return redirect(url_for('latedrop'))
        
        drop_request.approver_id = approver.id

        db.session.add(drop_request)
        db.session.commit()
        prof_msg, student_msg = request_created(student, course.crn, " drop")
        subject = 'Drop Request'
        msg = Message(subject, recipients=[approver.email ], body = prof_msg)
        msg2 = Message(subject, recipients=[student.email], body = student_msg)
        mail.send(msg)
        mail.send(msg2)
        flash('Your late drop request has been submitted', 'success')
        return redirect(url_for('latedrop'))
    return render_template('latedrop.html', title='Late Drop Request', form=form)


@app.route('/requests', methods = ['GET', 'POST'])
def requests():
    form = FilterForm()
    return render_template('requests.html', form=form)


@app.route('/studentHome')
@login_required
def studentHome():
    return render_template('studentHome.html')


@app.route('/approverHome', methods=['GET', 'POST'])
def approverHome():
    add_requests = Request.query.filter_by(type = "Late Add", approver_id=current_user.id).all()
    drop_requests = Request.query.filter_by(type = "Drop", approver_id=current_user.id).all()
    if current_user.role == "approver":
        title = "Approver Home"
    else:
        title = "Registrar Home"

    return render_template('approverHome.html', title=title, add_requests=add_requests, drop_requests=drop_requests)

@app.route('/trackRequest',methods=['GET'])
@login_required
def trackRequest():
    all_requests = Request.query.filter_by(student_id=current_user.id).all()
    requests = []
    for request in all_requests:
        course = Course.query.filter_by(crn = request.course_id).first()
        status = RequestStatus.query.filter_by(id = request.status_id).first()
        requests.append((request.date, str(request.timestamp),request.type, course.subject, course.course, course.section, course.crn, status.status, request.comments))
    return render_template('trackRequest.html', requests = requests)

@app.route('/viewRequest', methods=['GET', 'POST'])
@login_required
def viewRequest():
    print("View Request route called")
    form = ViewRequestForm()
    approver_id = current_user.id
    all_requests = Request.query.filter_by(approver_id = approver_id).all()
    requests = []
    for request in all_requests:
        course = Course.query.filter_by(crn = request.course_id).first()
        status = RequestStatus.query.filter_by(id = request.status_id).first()
        student_id = request.student_id
        student = Student.query.filter_by(id = student_id).first()
        student_id = student.student_id
        requests.append((student.first_name, student.last_name, student_id, str(request.timestamp),request.type, course.subject, course.course, course.section, course.crn, request.comments, request.id, status.status))
        
    return render_template('viewRequest.html', form=form, requests=requests)

@app.route('/adminHome')
def adminHome():
    return render_template('adminHome.html')


@app.route('/updateRequest/<int:request_id>', methods=['POST'])
@login_required
def updateRequest(request_id):
    form = ViewRequestForm()
    request = Request.query.get(request_id)
    
    # Pending = 1
    # Approved = 2
    # Denied = 3
    # Returned = 4
    # Awaiting Registrar Approval = 5

    if form.validate_on_submit():
        # Update request status and comments based on the form data
        student = Student.query.filter_by(email = request.email ).first()
        print("status: " , request.status_id)
        if form.approve.data:
            if request.status_id == 5:
                request.status_id = 2
                request.approver_id = None
                
            elif request.status_id == 1:
                request.status_id = 5
                # update to registrar ID
                request.approver_id = 3
                approver = Approver.query.filter_by(id = request.approver_id).first()
                req_type = " " +request.type
                prof_msg, student_msg = request_created(student, request.course_id, req_type)
                subject = req_type +' Request'
                msg = Message(subject, recipients=[approver.email ], body = prof_msg)
                        
                
        elif form.deny.data:
            request.status_id = 3
            request.approver_id = None

        request.comments = form.comments.data

        # Save the changes to the database
        db.session.commit()
        course = Course.query.filter_by(crn = request.course_id).first()
        student_msg = status_change(student, course.crn)
        subject = 'Status Change'
        msg = Message(subject, recipients=[student.email], body = student_msg)
        mail.send(msg)

        # Redirect the user to the viewRequest page
        return redirect(url_for('viewRequest'))
    else:
        # If the form is not valid, render the requestDetails page with the existing data
        request = Request.query.get(request_id)
        student = Student.query.filter_by(id = request.student_id).first()
        course = Course.query.filter_by(crn = request.course_id).first()
        status = RequestStatus.query.filter_by(id = request.status_id).first()
        info = [(student.first_name, student.last_name, student.student_id,str(request.timestamp),request.type, course.subject, course.course, course.section, course.crn, request.term, request.comments, request.id, status.status)]
        return render_template('requestDetails.html', form=form, request=info)

@app.route('/requestDetails/<int:request_id>', methods=['GET', 'POST'])
@login_required
def requestDetails(request_id):
    form = ViewRequestForm()
    request = Request.query.get(request_id)
    # if request is None:
    #     request = Request.query.get(request_id)
    student = Student.query.filter_by(id = request.student_id).first()
    course = Course.query.filter_by(crn = request.course_id).first()
    status = RequestStatus.query.filter_by(id = request.status_id).first()
    # requests.append((student.first_name, student.last_name, student_id, str(request.timestamp),request.type, course.subject, course.course, course.section, course.crn, request.comments, request.id))
    
    info = [(student.first_name, student.last_name, student.student_id,str(request.timestamp),request.type, course.subject, course.course, course.section, course.crn, request.term, request.comments, request.id, status.status)]
    # info = (student.first_name, student.last_name, student.student_id,str(request.timestamp),request.type, course.subject, course.course, course.section, course.crn, request.term, request.comments, request.id)
    return render_template('requestDetails.html', form=form, request=info)

@app.route('/reports', methods = ['GET', 'POST'])
def reports():
    form = ReportsForm()
    return render_template('reports.html', form=form)
