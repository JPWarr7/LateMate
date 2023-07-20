
from app import db
from app.models import User, Student, Approver, Course, RequestStatus
import pandas as pd

def populate_db():
    # create a few users
    users = [
        # ('John', 'Doe', 'jdoe', 'jdoe@example.com', 'password', 'approver'),
        # ('Jane', 'Doe', 'jane', 'jane@example.com', 'password', 'approver'),
        # ('Bob', 'Smith', 'bsmith', 'bsmith@example.com', 'password', 'approver'),
        # ('Gary', 'Warren', 'gwarren', 'gwarren@example.com', 'password', 'approver'),
        # ('Sam', 'Ortiz', 'sortiz', 'sortiz@example.com', 'password', 'approver'),
        # ('Mary', 'Escalona', 'mescalona', 'mescalona@example.com', 'password', 'approver'),
        ('Timmy', 'Turner', 'Timt', 'TT@example.com', 'password', 'student'),
        ('Sam', 'Gane', 'SGane', 'GG@example.com', 'password', 'student'),
        ('Example', 'Registrar', 'Registrar', 'csc330.latemate@gmail.com', 'password', 'approver')
    ]

    for first_name, last_name, student_id, email, password, role in users:
        if role == 'student':
            student = Student(first_name=first_name, last_name=last_name, student_id=student_id, email=email, role=role, major="Example Major", gpa=3.5)
            student.set_password(password)
            db.session.add(student)
        elif role in ('approver'):
            approver = Approver(first_name=first_name, last_name=last_name, student_id=student_id, email=email, role=role, department="Registrar")
            approver.set_password(password)
            db.session.add(approver)
        # elif role == 'registrar':
        #     approver = Registrar(first_name=first_name, last_name=last_name, student_id=student_id, email=email, role=role)
        #     approver.set_password(password)
        #     db.session.add(approver)


    # change folder_path according to your virtual machine    
    folder_path = "/home/jonathanwarren2022/ctrl-alt-elite-dev/FALL-2023-CSC-schedule.csv"

    # reading dataset
    courseFile = pd.read_csv(folder_path)

    # extracting vals
    crn = courseFile[['CRN']].to_dict('list')
    crnList = list(crn['CRN'])
    
    subject = courseFile[['SUB']].to_dict('list')
    subjectList = list(subject['SUB'])
    
    course = courseFile[['CRSE']].to_dict('list')
    courseList = list(course['CRSE'])
    
    section = courseFile[['SEC']].to_dict('list')
    sectionList = list(section['SEC'])
    
    instructor = courseFile[['INSTRUCTOR']].to_dict('list')
    instructorList = list(instructor['INSTRUCTOR'])
    
    uniqueInstructors = []
    for i in instructorList:
            if i not in uniqueInstructors:
                uniqueInstructors.append(i)
    x = 0
    for name in uniqueInstructors:
        title = name
        name = name.split(',')
        
        approver = Approver(first_name=name[1], last_name=name[0], student_id=name[0], email='warrenj8@southernct.edu', role='approver', department=subjectList[0], title = title)
        approver.set_password(str(x))
        print(f'Setting password for {name[1]} {name[0]} to {x}')
        db.session.add(approver)
        x+=1
    
    db.session.commit() # added commit to pull approvers for courses. 
    
    for i in range(len(instructorList)):
        name = instructorList[i].split(',')
        approver = Approver.query.filter_by(title = instructorList[i]).first()
        course = Course(crn = int(crnList[i]), subject = subjectList[i], course = courseList[i],section = sectionList[i],instructor = instructorList[i], professor_id = approver.id)
        db.session.add(course)
            
    status_list = ['Pending', 'Approved', 'Denied', 'Returned', 'Awaiting Registrar Approval']

    for i, status in enumerate(status_list, start=1):
        new_status = RequestStatus(id=i, status=status)
        db.session.add(new_status)
     
    db.session.commit() 

if __name__ == '__main__':
    populate_db()


