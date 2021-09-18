import enum
import numpy as np
from database import models
from repository import Schemas, attendence
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from fastapi import HTTPException, status, Response
from datetime import datetime

# Teacher

def get_messages(db: Session, new_five: bool):
    fake_dep = "bca"
    messages = db.query(models.Message).filter(
                or_(models.Message.hod_department == fake_dep,
                    models.Message.hod_department == "all")
            ).all()
    if new_five: return messages[::-1][:5]
    return messages[::-1]

def get_hour_detail(db: Session):
    fake_teacher = 'arjun_bca'
    fake_day = datetime.today().strftime("%A")
    fake_day = "Monday"

    classes = db.query(models.Timetable).filter(
            and_(models.Timetable.days == fake_day,
                or_(
                    models.Timetable.hour_1 == fake_teacher,
                    models.Timetable.hour_2 == fake_teacher,
                    models.Timetable.hour_3 == fake_teacher,
                    models.Timetable.hour_4 == fake_teacher,
                    models.Timetable.hour_5 == fake_teacher
                )
            )
        ).all()

    return get_hour(classes, fake_teacher)

def get_hour(classes, teacher_name):
    full_data = []

    for data in classes:
        course = data.course.upper()
        year = data.year
        hours = [data.hour_1, data.hour_2, data.hour_3, data.hour_4, data.hour_5]
        for i, name in enumerate(hours, start=1):
            if teacher_name == name:
                s = Schemas.HourDetails(course = course, hour = i, year = year)
                full_data.append(s)

    return full_data


# Students

def add_student(request: Schemas.AddStudent, db: Session):

    res = attendence.admit_students(request=request, save_monthly=True)

    new_student = models.Students(
                    id = request.unique_id, name = request.name,\
                    email = request.email, parent_name = request.parent_name,\
                    parent_number = request.parent_number,\
                    parent_number_alt = request.number, course = request.course,\
                    year = request.year
                )

    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return res


def delete_student(request: Schemas.DeleteStudent, db: Session):

    student = db.query(models.Students).filter(and_(models.Students.name == request.name,\
                                models.Students.id == request.unique_id,\
                                models.Students.year == request.year,
                                models.Students.course == request.course
                            ))

    if not student.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Alert No User in database") 

    student.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=204)


def edit_verify_student(request: Schemas.DeleteStudent, db: Session):

    student = db.query(models.Students).filter(
                and_(
                    models.Students.id == request.unique_id,
                    models.Students.name == request.name,
                    models.Students.course == request.course,
                    models.Students.year == request.year
                )).first()

    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Alert No User in database") 

    response = Schemas.AddStudent(unique_id = student.id, name = student.name, email = student.email,\
                       parent_name = student.parent_name, parent_number = student.parent_number,
                       number = student.parent_number_alt, course = student.course,
                       year = student.year
                    )

    return response


def edit_student(request: Schemas.EditStudent, db: Session):
    student = db.query(models.Students).filter(
                    and_(
                        models.Students.id == request.old_unique_id,
                        models.Students.name == request.old_name,
                        models.Students.course == request.old_course,
                        models.Students.year == request.old_year)
                    )

    if not student.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not Found")
    
    updated_details = {'id': request.unique_id, 'name': request.name, 'email': request.email,
                       'parent_name': request.parent_name, 'parent_number': request.parent_number,
                       'parent_number_alt': request.number, 'course': request.course, 
                       'year': request.year}

    student.update(updated_details)
    
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)