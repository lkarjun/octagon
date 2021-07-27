from sqlalchemy.orm.session import Session
from database import models
from security import hashing
from fastapi import status, HTTPException, Response
from sqlalchemy import and_, or_
from repository.attendence import CreateAttendence
from repository import Schemas

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

def get_all(db: Session):
    hods = db.query(models.Hod).all()
    if not hods:
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
    hod = db.query(models.Hod).filter(and_(models.Hod.user_name == request.name,
                                models.Hod.department == request.department))
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

def new_department(request: Schemas.AddDepartment, db: Session):
    department = models.Departments(Department = request.Department, Alias = request.Alias)
    db.add(department)
    db.commit()
    db.refresh(department)
    return "Department Added"

def get_all_departments(db: Session):
    departments = db.query(models.Departments).all()
    if not departments:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,\
            detail = 'No content in the database')
    return departments

def delete_department(request: Schemas.DeleteDepartment, db: Session):
    depart = db.query(models.Departments).filter(models.Departments.Alias == request.department)
    if not depart.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,\
                    detail=f"No Department in name {request.Department} and alias {request.Alias}") 
    depart.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=204)

def add_course(request: Schemas.AddCourse, db: Session):
    course = models.Courses(Course_name = request.course_name, Course_name_alias = request.course_alias,
                            Department = request.department,
                            Duration = request.duration)
    CreateAttendence(request.duration, request.course_alias)
    db.add(course)
    db.commit()
    db.refresh(course)
    return "Course Added"

def delete_course(request: Schemas.DeleteCourse, db: Session):
    course = db.query(models.Courses).filter(models.Courses.Course_name_alias == request.course_name)
    if not course.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,\
                    detail=f"No Course in name {request.course_name}")

    course.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=204)

def get_all_course(db: Session):
    courses = db.query(models.Courses).all()
    if not courses:
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
