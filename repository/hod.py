import Schemas, models
from sqlalchemy.orm import Session
from sqlalchemy import and_
from fastapi import HTTPException, status, Response
from . import mail_it

def create(request: Schemas.AddTeacher, db: Session):
    new_teacher = models.Teachers(
                    name = request.name, email = request.email,\
                    phone_number = request.phone_number, department = request.department
                )
    
    db.add(new_teacher)
    db.commit()
    db.refresh(new_teacher)
    return new_teacher

def delete(name: str, email: str, db: Session):
    teacher = db.query(models.Teachers).filter(and_(models.Teachers.name == name,
                                models.Teachers.email == email))
    if not teacher.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Alert No User with name: {name} and email: {email}") 

    teacher.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=204)

def update(email: str, request: Schemas.AddTeacher, db: Session):
    teacher = db.query(models.Teachers).filter(models.Teachers.email == email)
    if not teacher.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Alert No User with email: {email}")
    teacher.update(dict(request))
    db.commit()
    return 'done'

def get_techer_details(db: Session):
    teachers = db.query(models.Teachers).all()
    if not teachers:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,\
            detail = 'No content in the database')
    return teachers

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

def check_timetable(request: Schemas.TimeTableChecker, db: Session, conflict = True):
    print(helper_timetable_check(request.hour))
    checker = db.query(models.Timetable).filter(and_(
                        models.Timetable.days == request.day,
                        helper_timetable_check(request.hour) == request.name
                )).all()

    if checker and conflict:
        name = [conflict_name(teacher, request.hour) for teacher in checker]
        print(name)
        return name
    else: print('NO')

def display_timetable(course: str, year: int, db: Session):
    timetable = db.query(models.Timetable).filter(and_(models.Timetable.year == year,
                                models.Timetable.course == course))
    if not timetable.first(): return 'No'

    result = {'Monday': [], 'Tuesday': [], 'Wednesday': [], 'Thursday': [], 'Friday': []}

    for i, day in zip(timetable, result):
        result[day].append(i.hour_1)
        result[day].append(i.hour_2)
        result[day].append(i.hour_3)
        result[day].append(i.hour_4)
        result[day].append(i.hour_5)
    return result

def remove_timetable(course: str, year: int, db: Session):
    timetable = db.query(models.Timetable).filter(and_(models.Timetable.course == course,
                                models.Timetable.year == year))

    if not timetable:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No Timetable sets course: {course} and year: {year}") 
    timetable.delete(synchronize_session=False)
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
