from sqlalchemy.orm.session import Session
from database import models
from security import hashing, faceid
from fastapi import status, HTTPException, Response
from sqlalchemy import and_, or_
from repository import Schemas, attendence
import time

def change_admin_pass(request: Schemas.AdminPass, db: Session):
    admin_pass = db.query(models.Admin).filter(models.Admin.name == request.username)
    
    if not admin_pass.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid Credentials")
    
    if not hashing.Hash.verify(admin_pass.first().password, request.current_pass):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Incorrect password")
    # generate a jwt token and return it
    updating = {'name': request.username, 'password': hashing.Hash.bcrypt(request.new_pass)}
    admin_pass.update(updating)
    db.commit()
    return 'changed'

def get_all(db: Session, template=False):
    hods = db.query(models.Hod).all()
    if not hods:
        if template: return []
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,\
            detail = 'No content in the database')
    return hods

def get_one(db: Session, user_name: str):
    if user_name is None: return 'Please pass hod name to get details'
    hod = db.query(models.Hod).filter(models.Hod.user_name == user_name).first()
    if not hod:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,\
            detail = f'THERE IS NO HOD IN USER NAME: {user_name}')
    return hod  

def update(user_name: str, request: Schemas.CreateHod, db: Session):
    hod = db.query(models.Hod).filter(models.Hod.user_name == user_name)
    if not hod.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Alert No User with {user_name}") 
    hod.update(dict(request))
    db.commit()
    return 'done'

def delete(request: Schemas.DeleteHod, db: Session):
    hod = db.query(models.Hod).filter(models.Hod.user_name == request.username)
    
    if not hod.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Alert No User with name: {request.name} and department: {request.department}") 

    hod.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=204)

def create(request: Schemas.CreateHod, db: Session):
    user_name_check = db.query(models.Hod).filter(or_(
                        models.Hod.user_name == request.user_name,
                        models.Hod.email == request.email,
                        models.Hod.phone_num == request.phone_num
                    )).first()
    if user_name_check:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                                detail = f"User already exists: check username '{request.user_name}', email '{request.email}', phone number '{request.phone_num}'")

    new_hod = models.Hod(name = request.name, email = request.email, \
                        phone_num = request.phone_num, user_name = request.user_name, \
                        department = request.department)
    db.add(new_hod)
    db.commit()
    db.refresh(new_hod)
    return True

def verification_image(username, image1, image2, image3):
    print("Getting encodings for images at", time.strftime("%H:%M:%S", time.localtime()))
    encodings = faceid.read_images(image1, image2, image3)
    print("Saving encoded vectors at", time.strftime("%H:%M:%S", time.localtime()))
    faceid.put_faces(username, encodings)
    print("Saved encoded vectors at", time.strftime("%H:%M:%S", time.localtime()))
    return Response(status_code=204)

def new_department(request: Schemas.AddDepartment, db: Session):
    department = models.Departments(Department = request.Department, Alias = request.Alias)
    db.add(department)
    db.commit()
    db.refresh(department)
    return "Department Added"

def get_all_departments(db: Session, template=False):
    departments = db.query(models.Departments).all()
    if not departments:
        if template: return []
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,\
            detail = 'No content in the database')
    return departments

def delete_department(request: Schemas.DeleteDepartment, db: Session):
    depart = db.query(models.Departments).filter(models.Departments.Alias == request.department)
    hod = db.query(models.Hod).filter(models.Hod.department == request.department)
    teacher = db.query(models.Teachers).filter(models.Teachers.department == request.department)
    timetable = db.query(models.Timetable).filter(models.Timetable.department == request.department)
    timetableS = db.query(models.TimetableS).filter(models.TimetableS.department == request.department)
    students = db.query(models.Students).filter(models.Students.department == request.department)
    course = db.query(models.Courses).filter(models.Courses.Department == request.department)
    
    if not depart.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,\
                    detail=f"No Department in name {request.Department} and alias {request.Alias}")
    
    depart.delete(synchronize_session=False)
    if teacher.first(): teacher.delete(synchronize_session=False)
    if hod.first(): hod.delete(synchronize_session=False)
    if timetableS.first(): timetableS.delete(synchronize_session=False)
    if timetable.first(): timetable.delete(synchronize_session=False)
    if students.first(): students.delete(synchronize_session=False)
    if course.first():
        for i in course:
            attendence.deleteAttendence(i.Duration, i.Course_name_alias)
        course.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=204)

def add_course(request: Schemas.AddCourse, db: Session):
    course = models.Courses(Course_name = request.course_name, Course_name_alias = request.course_alias,
                            Department = request.department,
                            Duration = request.duration)
    attendence.createAttendence(request.duration, request.course_alias)
    db.add(course)
    db.commit()
    db.refresh(course)
    return "Course Added"

def delete_course(request: Schemas.DeleteCourse, db: Session):
    course = db.query(models.Courses).filter(models.Courses.Course_name_alias == request.course_name)
    if not course.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,\
                    detail=f"No Course in name {request.course_name}")
    course_ = course.first()
    attendence.deleteAttendence(course_.Duration, course_.Course_name_alias)
    course.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=204)

def get_all_course(db: Session, template=False):
    courses = db.query(models.Courses).all()
    if not courses:
        if template: return []
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,\
            detail = 'No content in the database')
    return courses

def reset_pass(request: Schemas.AdminPass, db: Session):
    current = db.query(models.Admin).filter(models.Admin.name == request.username)
    if not hashing.Hash.verify(current.first().password, request.current_pass):
        raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, detail="Wrong password")
    if not current.first():
        raise HTTPException(status.HTTP_203_NON_AUTHORITATIVE_INFORMATION, detail="Something Went wrong")
    hashing_pass = hashing.Hash.bcrypt(request.new_pass)
    current.update({'name': request.username, 'password': hashing_pass})
    db.commit()
    return "Password changed successfully..."
