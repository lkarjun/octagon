from database import models
from repository import Schemas,uoc, attendence
from sqlalchemy.orm import Session
from sqlalchemy import and_
from fastapi import HTTPException, status, Response, BackgroundTasks, UploadFile
from security import faceid, hashing
from octagonmail import octagonmail
from tqdm import tqdm
import pandas as pd
from datetime import date

#================================v2.0===========================================
def appoint_teacher_v2_0(data: Schemas.Staff_v2_0, db: Session, bg_task: BackgroundTasks):
    new_teacher = models.Teachers(**data.dict())
    id = hashing.get_unique_id(data.username)
    pending_verification = models.PendingVerificationImage(
                            id=id, 
                            user_username=data.username, 
                            user_email = data.email, 
                            hod_or_teacher='T')
    db.add(new_teacher)
    db.add(pending_verification)
    db.commit()
    db.refresh(new_teacher)
    bg_task.add_task(octagonmail.verification_mail, data.name, data.email, id)
    return Response(status_code=204)

def appoint_teacher_v2_0_from_file(Data: UploadFile, department:str, db: Session, bg_task: BackgroundTasks):
    if Data.content_type == "text/csv":
        df = pd.read_csv(Data.file)
    elif Data.content_type == 'text/xlxm' or Data.content_type == 'text/xls':
        df = pd.read_excel(Data.file)
    else: raise HTTPException(status_code=status.HTTP_304_NOT_MODIFIED, detail="dataformat mismatched")

    for _, i in tqdm(df.iterrows(), colour='green', desc='Adding Teachers from File'): 
        i['department'] = department
        i['username'] = form_username(i['name'], i['phone_num'])
        i = Schemas.Staff_v2_0(**i.to_dict())
        res = appoint_teacher_v2_0(i, db, bg_task)
        if not res:
            print(f"Failed to add student: {i.name} {i.id}")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

def form_username(name: str, phone: int, scode: int = 1111):
    phone = str(phone)
    username = f"{name[:3]}{phone[7:]}{scode}"
    return username.lower()

def change_status(request: Schemas.Staff_v2_0_status, db: Session):
    if request.status != "Continue":
        dis_status = str(date.today()) 
    else: dis_status = "-"
    teacher_db = db.query(models.Teachers).filter(models.Teachers.username == request.username)
    teacher = teacher_db.first()
    if not teacher:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Alert No User with name: {request.name} and department: {request.department}") 
    hod_dict = {'id': teacher.id, 'name': teacher.name, 'username': teacher.username, 'email': teacher.email, 'phone_num': teacher.phone_num, 'department': teacher.department, 'tag': teacher.tag
                ,'joining_date': teacher.joining_date, 'dob': teacher.dob, 'higher_qualification': teacher.higher_qualification, 'net_qualification': teacher.net_qualification,
                'designation': teacher.designation, 'gender': teacher.gender, 'teaching_experience': teacher.teaching_experience, 'religion': teacher.religion,
                'social_status': teacher.social_status, 'status': request.status, 'discontinued_date': dis_status}
    teacher_db.update(hod_dict)
    db.commit()
    return Response(status_code=204)

def check_st_details(request: Schemas.TerminalZone, db: Session):
    if request.action == 'detail_check':
        tmp = get_student_details(db, request.course, request.year)
    else:
        attendence._check_attendence_data(request)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    
#===========================================================================

def appoint_teacher(request: Schemas.AddTeacher, db: Session, bg_task: BackgroundTasks):
    new_teacher = models.Teachers(
                    name = request.name, email = request.email,\
                    phone_num = request.phone_num,\
                    department = request.department, tag = request.tag,\
                    username = request.username
                )
    id = hashing.get_unique_id(request.username)
    pending_verification = models.PendingVerificationImage(
                            id=id, 
                            user_username=request.username, 
                            user_email = request.email, 
                            hod_or_teacher='T')
    db.add(new_teacher)
    db.add(pending_verification)
    db.commit()
    db.refresh(new_teacher)
    bg_task.add_task(octagonmail.verification_mail, request.name, request.email, id)
    return Response(status_code=204)

def remove_teacher(request: Schemas.DeleteTeacher, db: Session):
    teacher = db.query(models.Teachers).filter(and_(models.Teachers.id == request.name,
                                models.Teachers.username == request.username))
    pending_verification = db.query(models.PendingVerificationImage).filter(models.PendingVerificationImage.user_username == request.username)
    if not teacher.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Alert No User in database") 

    if pending_verification.first():
        pending_verification.delete(synchronize_session=False)
    
    teacher.delete(synchronize_session=False)
    remove_encoding = faceid.remove_encoding(request.username)
    # if not remove_encoding:
    #     raise HTTPException(status_code=status.HTTP_304_NOT_MODIFIED, 
    #                   detail = f"Failed to remove encodings for the user: {request.username}")
    db.commit()
    return Response(status_code=204)

def terminalzone(request: Schemas.TerminalZone, db: Session, user):
    if request.action == 'Start New Semester':
        
        attendence.start_new_semester(
                        request = request,
                        open_monthly = True,
                        save_monthly = True,
        )


    elif request.action == 'Promote Students':

        course_duration = db.query(models.Courses).filter(models.Courses.Course_name_alias == request.course).first()
        if request.year > course_duration.Duration:
            raise HTTPException(
                status.HTTP_406_NOT_ACCEPTABLE, 
                detail="Course duration is not correct! Please check you've entered the correct duration or not."
                )
        if request.year == course_duration.Duration: 
            raise HTTPException(
                status.HTTP_406_NOT_ACCEPTABLE, 
                detail="We can't promote students, these students are final years."
                )
        attendence.promote_students(request=request, 
                                    open_monthly = True,
                                    save_monthly = True,
                                    db=db, user=user)
    else:
        
        attendence.remove_students_for_new_semester(request = request, db = db, user = user)

    return Response(status_code=status.HTTP_204_NO_CONTENT)

def update(email: str, request: Schemas.AddTeacher, db: Session):
    teacher = db.query(models.Teachers).filter(models.Teachers.email == email)
    if not teacher.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Alert No User with email: {email}")
    teacher.update(dict(request))
    db.commit()
    return 'done'

def get_techer_details(db: Session, user, template=False):
    teachers = db.query(models.Teachers).filter(models.Teachers.department == user.department)
    if not teachers:
        if template: return []
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,\
            detail = 'No content in the database')
    return teachers

def get_full_teacher_details(db: Session):
    teachers = db.query(models.Teachers).all()
    if not teachers: return []
    return teachers

def get_student_details(db: Session, course: str, year: int, template = False):
    student = db.query(models.Students).filter(models.Students.course == course,\
                            models.Students.year == year).all()
    if not student:
        if template: return False
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = 'Not admitted students...')
    return student

def send_message(user, request: Schemas.Message, db: Session):

    hod_name = user.username
    hod_dep = user.department

    message = models.Message(
        hod_name = hod_name, hod_department = hod_dep,
        date = request.date, to = request.to, title = request.title,
        message = request.message, important = request.important
    )
    db.add(message)
    db.commit()
    db.refresh(message)

    return Response(status_code=status.HTTP_204_NO_CONTENT)

def get_full_message(db: Session, user):
    hod_name = user.username
    hod_dep = user.department
    messages = db.query(models.Message).filter(
                and_(models.Message.hod_name == hod_name,
                    models.Message.hod_department == hod_dep)
            ).all()
    return messages[::-1]

def clear_message(db: Session, user):
    hod_name = user.username
    hod_dep = user.department
    messages = db.query(models.Message).filter(
        and_(models.Message.hod_name == hod_name,
             models.Message.hod_department == hod_dep)
        )
    if not messages.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Alert No Messages in database")
    
    messages.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=204)
    

def mail_(who: str, message: str, db: Session):
    message = message.replace('\\n', '\n').replace('\\t', '\t')
    if who == 'hod':
        email = db.query(models.Hod).all()
        emails = [mail_id.email for mail_id in email]
        emails = ','.join(emails)
        return mail_it.Annousement_to_hods(emails, 'NotFixed', message)

    email = db.query(models.Teachers).all()
    emails = [mail_id.email for mail_id in email]
    emails = ','.join(emails)
    return mail_it.Annousement_to_hods(emails, 'NotFixed-Teacher', message)

def set_timetable(request: Schemas.TimeTable, db: Session):
    data = [request.day_1, request.day_2, request.day_3, request.day_4, request.day_5]
    data_subject = [request.sub_day_1, request.sub_day_2, request.sub_day_3, request.sub_day_4,
                    request.sub_day_5]

    for i, d1 in enumerate(data_subject):
        hours = models.TimetableS(
                    department = request.department, 
                    course = request.course,
                    year = request.year,
                    days = request.days[i],
                    hour_1 = d1[0],
                    hour_2 = d1[1],
                    hour_3 = d1[2],
                    hour_4 = d1[3],
                    hour_5 = d1[4]
            )  
        db.add(hours)
        db.commit()
        db.refresh(hours)
    
    for i, d1 in enumerate(data):
        hours = models.Timetable(
                    department = request.department, 
                    course = request.course,
                    year = request.year,
                    days = request.days[i],
                    hour_1 = d1[0],
                    hour_2 = d1[1],
                    hour_3 = d1[2],
                    hour_4 = d1[3],
                    hour_5 = d1[4]
            )  
        db.add(hours)
        db.commit()
        db.refresh(hours)
    return 'okay'

def check_timetable(request: Schemas.TimeTableChecker, db: Session):
    name = db.query(models.Teachers).filter(models.Teachers.username == request.name).first()
    if not name:
        name = db.query(models.Hod).filter(models.Hod.username == request.name).first()
        username = name.username
    else: username = name.username
    checker = db.query(models.Timetable).filter(and_(
                        models.Timetable.days == request.day,
                        helper_timetable_check(request.hour) == username,
                )).first()
    if checker: raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, detail=f"{request.day} {request.hour} {name.name} have class in {checker.course} year {checker.year}...")
    return "No Issue..."
    

def display_timetable(request: Schemas.TimeTableEdit, db: Session):
    timetable = db.query(models.TimetableS).filter(and_(models.TimetableS.year == request.year,
                                models.TimetableS.course == request.course))
    if not timetable.first(): raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No Timetable sets course: {request.course} and year: {request.year}")

    result = {'Monday': [], 'Tuesday': [], 'Wednesday': [], 'Thursday': [], 'Friday': []}

    for i, day in zip(timetable, result):
        result[day].append(i.hour_1)
        result[day].append(i.hour_2)
        result[day].append(i.hour_3)
        result[day].append(i.hour_4)
        result[day].append(i.hour_5)
    return result

def remove_timetable(request: Schemas.TimeTableEdit, db: Session):
    timetable = db.query(models.Timetable).filter(and_(models.Timetable.course == request.course,
                                models.Timetable.year == request.year,
                                models.Timetable.department == request.department))
    timetableS = db.query(models.TimetableS).filter(and_(models.TimetableS.course == request.course,
                                models.TimetableS.year == request.year,
                                models.TimetableS.department == request.department))
    if not timetable.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No Timetable sets course: {request.course} and year: {request.year}") 
    timetable.delete(synchronize_session=False)
    timetableS.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=204)

def current_hour_detail(department: str, day: str, hour: str, db: Session):
    current_hour = db.query(models.Timetable).filter(and_(
                        models.Timetable.department == department,
                        models.Timetable.days == day
                    )).all()
    if not current_hour:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,\
            detail = 'No content in the database')
    
    detail =  [Schemas.CurrentHour(name=conflict_name(i, hour), 
                                   course=i.course, year=i.year, 
                                   hour=hour) 
                        for i in current_hour]
    return detail

def update_profile(request: Schemas.Staff_v2_0, db: Session, user: models.Hod):
    userdetail = db.query(models.Hod).filter(
                    and_(models.Hod.username == user.username,
                         models.Hod.id == user.id))
    userdetail.update(dict(request))
    faceid.update_username(user.username, request.username)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

#helper function
def helper_timetable_check(hour: str):
    '''helper function for check timetable.'''
    if hour == 'hour_1': return models.Timetable.hour_1
    elif hour == 'hour_2': return models.Timetable.hour_2
    elif hour == 'hour_3': return models.Timetable.hour_3
    elif hour == 'hour_4': return models.Timetable.hour_4
    else: return models.Timetable.hour_5

def conflict_name(teacher, hour):
    if hour == 'hour_1': return teacher.hour_1
    elif hour == 'hour_2': return teacher.hour_2
    elif hour == 'hour_3': return teacher.hour_3
    elif hour == 'hour_4': return teacher.hour_4
    else: return teacher.hour_5
