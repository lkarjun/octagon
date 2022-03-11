from typing import Dict
from sqlalchemy.orm.session import Session
from database import models
from security import hashing, faceid
from fastapi import status, HTTPException, Response, BackgroundTasks, UploadFile
from sqlalchemy import and_, or_
from repository import Schemas, attendence
import time
from octagonmail import octagonmail
import pandas as pd
from tqdm import tqdm
from datetime import date

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

def get_one(db: Session, username: str):
    if username is None: return 'Please pass hod name to get details'
    hod = db.query(models.Hod).filter(models.Hod.username == username).first()
    if not hod:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,\
            detail = f'THERE IS NO HOD IN USER NAME: {username}')
    return hod  

def update(username: str, request: Schemas.CreateHod, db: Session):
    hod = db.query(models.Hod).filter(models.Hod.username == username)
    if not hod.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Alert No User with {username}") 
    hod.update(dict(request))
    db.commit()
    return 'done'

def delete(request: Schemas.DeleteHod, db: Session):
    hod = db.query(models.Hod).filter(models.Hod.username == request.username)
    pending_verification = db.query(models.PendingVerificationImage).filter(models.PendingVerificationImage.user_username == request.username)
    if not hod.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Alert No User with name: {request.name} and department: {request.department}") 

    hod.delete(synchronize_session=False)
    if pending_verification.first():
        pending_verification.delete(synchronize_session=False)
    remove_encoding = faceid.remove_encoding(request.username)
    # if not remove_encoding:
    #     print("THIS is wokring")
    #     raise HTTPException(status_code=status.HTTP_304_NOT_MODIFIED, 
    #                   detail = f"Failed to remove encodings for the user: {request.username}")
    db.commit()
    return Response(status_code=204)

# ======================================V2.0=========================================================
# Changes needed here

def appoint_hod(data: Schemas.Staff_v2_0, db: Session, bg_task: BackgroundTasks):
    username_check = db.query(models.Hod).filter(or_(
                            models.Hod.id == data.id,
                            models.Hod.username == data.username
                            ))

    if username_check.first():
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                                detail = f"User already exists: check username '{data.username}', id '{data.id}', phone number '{data.phone_num}'")

    new_hod = models.Hod(**data.dict())
    id = hashing.get_unique_id(data.username)
    pending_verification = models.PendingVerificationImage(
                            id=id, 
                            user_username=data.username, 
                            user_email = data.email, 
                            hod_or_teacher='H')
    db.add(new_hod)
    db.add(pending_verification)
    db.commit()
    db.refresh(new_hod)
    bg_task.add_task(octagonmail.verification_mail, data.name, data.email, id)
    return Response(status_code=204)


def appoint_hod_v2_0_from_file(Data: UploadFile, db: Session, bg_task: BackgroundTasks):
    if Data.content_type == "text/csv":
        df = pd.read_csv(Data.file)
    elif Data.content_type == 'text/xlxm' or Data.content_type == 'text/xls':
        df = pd.read_excel(Data.file)
    else: raise HTTPException(status_code=status.HTTP_304_NOT_MODIFIED, detail="dataformat mismatched")

    for _, i in tqdm(df.iterrows(), colour='green', desc='Adding hod from File'): 
        i['username'] = form_username(i['name'], i['phone_num'])
        i = Schemas.Staff_v2_0(**i.to_dict())
        res = appoint_hod(i, db, bg_task)
        if not res:
            print(f"Failed to add student: {i.name} {i.id}")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

def form_username(name: str, phone: int, scode: int = 1111):
    phone = str(phone)
    username = f"{name[:3]}{phone[7:]}{scode}"
    return username

def change_status(request: Schemas.Staff_v2_0_status, db: Session):
    if request.status != "Continue":
        dis_status = str(date.today()) 
    else: dis_status = "-"

    hod_db = db.query(models.Hod).filter(models.Hod.username == request.username)
    hod = hod_db.first()
    if not hod:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Alert No User with name: {request.name} and department: {request.department}") 
    hod_dict = {'id': hod.id, 'name': hod.name, 'username': hod.username, 'email': hod.email, 'phone_num': hod.phone_num, 'department': hod.department, 'tag': hod.tag
                ,'joining_date': hod.joining_date, 'dob': hod.dob, 'higher_qualification': hod.higher_qualification, 'net_qualification': hod.net_qualification,
                'designation': hod.designation, 'gender': hod.gender, 'teaching_experience': hod.teaching_experience, 'religion': hod.religion,
                'social_status': hod.social_status, 'status': request.status, 'discontinued_date': dis_status}
    hod_db.update(hod_dict)
    db.commit()
    return Response(status_code=204)
# =================================================================================================

def create(request: Schemas.CreateHod, db: Session, bg_task: BackgroundTasks):
    username_check = db.query(models.Hod).filter(or_(
                        models.Hod.username == request.username,
                        models.Hod.email == request.email,
                        models.Hod.phone_num == request.phone_num
                    )).first()
    if username_check:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                                detail = f"User already exists: check username '{request.username}', email '{request.email}', phone number '{request.phone_num}'")

    new_hod = models.Hod(name = request.name, email = request.email, \
                        phone_num = request.phone_num, username = request.username, \
                        department = request.department)
    id = hashing.get_unique_id(request.username)
    pending_verification = models.PendingVerificationImage(
                            id=id, 
                            user_username=request.username, 
                            user_email = request.email, 
                            hod_or_teacher='H')
                
    db.add(new_hod)
    db.add(pending_verification)
    db.commit()
    db.refresh(new_hod)
    bg_task.add_task(octagonmail.verification_mail, request.name, request.email, id)
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
            attendence.deleteAttendenceFiles(i.Duration, i.Course_name_alias)
        course.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=204)

def add_course(request: Schemas.AddCourse, db: Session):
    course = models.Courses(Course_name = request.course_name, Course_name_alias = request.course_alias,
                            Department = request.department,
                            Duration = request.duration)
    attendence.createAttendenceFiles(request.duration, request.course_alias)
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
    attendence.deleteAttendenceFiles(course_.Duration, course_.Course_name_alias)
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
