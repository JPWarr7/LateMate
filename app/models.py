from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    student_id = db.Column(db.String(32), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    role = db.Column(db.String(32), nullable=False)
    
    __mapper_args__ = {
        'polymorphic_identity': 'user',
        'polymorphic_on': role
    }

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def is_active(self):
        # return True if the user is active
        return True
    
    def get_id(self):
        return str(self.id)

    @property
    def is_authenticated(self):
        return True

class Student(User):
    __tablename__ = 'student'

    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    major = db.Column(db.String(50), nullable=False)
    gpa = db.Column(db.Float, nullable=False)
    
    __mapper_args__ = {
        'polymorphic_identity': 'student',
    }

class Approver(User):
    __tablename__ = 'approver'

    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    department = db.Column(db.String(128), nullable=False)
    title = db.Column(db.String(50))

    __mapper_args__ = {
    'polymorphic_identity': 'approver',
    }
    
class Course(db.Model):
    __tablename__ = 'courses'
    
    crn = db.Column(db.Integer, primary_key = True)
    subject = db.Column(db.String(50))
    course = db.Column(db.String(50))
    section = db.Column(db.String(50))
    instructor = db.Column(db.String(50))
    professor_id = db.Column(db.Integer, db.ForeignKey('approver.id'))

class Request(db.Model):
    __tablename__ = 'request'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.Date, nullable=False)
    term = db.Column(db.String(32), nullable=False)
    student_id = db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.crn'), nullable=False)
    comments = db.Column(db.String(200))
    approver_id = db.Column(db.Integer, db.ForeignKey('approver.id'), nullable=True)
    status_id = db.Column(db.Integer, db.ForeignKey('request_status.id'))
    status = db.relationship('RequestStatus', backref='requests')
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    type = db.Column(db.String(32))
    
# class AddRequest(db.Model):
#     __tablename__ = 'add_request'

#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     date = db.Column(db.Date, nullable=False)
#     term = db.Column(db.String(32), nullable=False)
#     student_id = db.Column(db.String(32), nullable=False)
#     email = db.Column(db.String(50), nullable=False)
#     course_id = db.Column(db.Integer, db.ForeignKey('courses.crn'), nullable=False)
#     comments = db.Column(db.String(200))
#     approver_id = db.Column(db.Integer, db.ForeignKey('approver.id'), nullable=True)
#     status_id = db.Column(db.Integer, db.ForeignKey('request_status.id'))
#     status = db.relationship('RequestStatus', backref='add_requests')
#     timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
#     type = db.Column(db.String(32))

# class DropRequest(db.Model):
#     __tablename__ = 'drop_request'

#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     date = db.Column(db.Date, nullable=False)
#     term = db.Column(db.String(32), nullable=False)
#     student_id = db.Column(db.String(32), nullable=False)
#     email = db.Column(db.String(50), nullable=False)
#     course_id = db.Column(db.Integer, db.ForeignKey('courses.crn'), nullable=False)
#     comments = db.Column(db.String(200))
#     approver_id = db.Column(db.Integer, db.ForeignKey('approver.id'), nullable=True)
#     status_id = db.Column(db.Integer, db.ForeignKey('request_status.id'))
#     status = db.relationship('RequestStatus', backref='drop_requests')
#     timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
#     type = db.Column(db.String(32))

class RequestStatus(db.Model):
    __tablename__ = 'request_status'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    status = db.Column(db.String(32), nullable=False)