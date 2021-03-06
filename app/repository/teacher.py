from database import models
from repository import Schemas, attendence
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from fastapi import HTTPException, UploadFile, status, Response
from datetime import datetime
from security import faceid
import pandas as pd
from tqdm import tqdm
from io import StringIO

# Teacher

def update_profile(request: Schemas.Staff_v2_0, db: Session, user: models.Teachers):
    userdetail = db.query(models.Teachers).filter(
                    and_(models.Teachers.username == user.username,
                         models.Teachers.id == user.id))
    userdetail.update(dict(request))
    faceid.update_username(user.username, request.username)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

def get_messages(user, db: Session, new_five: bool):

    messages = db.query(models.Message).filter(
                or_(models.Message.hod_department == user.department,
                    models.Message.to == "all")
            ).all()
    if new_five: return messages[::-1][:2]
    return messages[::-1]

def get_hour_detail(db: Session, user: str, day=None):
    if not day: day = datetime.today().strftime("%A")

    classes = db.query(models.Timetable).filter(
            and_(models.Timetable.days == day,
                or_(
                    models.Timetable.hour_1 == user,
                    models.Timetable.hour_2 == user,
                    models.Timetable.hour_3 == user,
                    models.Timetable.hour_4 == user,
                    models.Timetable.hour_5 == user
                )
            )
        ).all()

    return get_hour(classes, user)

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

def my_timetable(db: Session, username: str):
    timetable = {
                    'Monday': sorted(get_hour_detail(db, username, day='Monday'), key=lambda x: x.hour),
                    'Tuesday': sorted(get_hour_detail(db, username, day='Tuesday'), key=lambda x: x.hour),
                    'Wednesday': sorted(get_hour_detail(db, username, day='Wednesday'), key=lambda x: x.hour),
                    'Thursday': sorted(get_hour_detail(db, username, day='Thursday'), key=lambda x: x.hour),
                    'Friday': sorted(get_hour_detail(db, username, day='Friday'), key=lambda x: x.hour)
                }
    return timetable


# Students


#===========================================v2.0================================
def add_students_from_file_helper(Data: UploadFile, db: Session):
    if Data.content_type == "text/csv":
        df = pd.read_csv(StringIO(str(Data.file.read(), 'utf-8')), encoding='utf-8')
    elif Data.content_type == 'text/xlxm' or Data.content_type == 'text/xls':
        df = pd.read_excel(StringIO(str(Data.file.read(), 'utf-8')), encoding='utf-8')
    else: raise HTTPException(status_code=status.HTTP_304_NOT_MODIFIED, detail="dataformat mismatched")
    # print(df)
    for _, i in tqdm(df.iterrows(), colour='green', desc='Adding Students from File'): 
        i = Schemas.Student_v2_0(**i.to_dict())
        res = add_student_v2_0(i, db)
        if not res:
            print(f"Failed to add student: {i.name} {i.id}")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    
def add_student_v2_0(request: Schemas.Student_v2_0, db: Session):
    df_file = pd.DataFrame({'ST_ID': [request.unique_id], 
                            'ST_NAME': [request.name], 
                            'ST_STATUS': [request.status]})
    res = attendence.admit_student_v2_0(df_file, request.course, request.year, if_exists='append')
    department = db.query(models.Courses).filter(models.Courses.Course_name_alias == request.course).first()
    request = request.dict()
    request['department'] = department.Department
    new_student = models.Students(**request)
    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return res

#===============================================================================


def add_student(request: Schemas.AddStudent, db: Session):

    res = attendence.admit_students(request=request, save_monthly=True, open_monthly=True)
    department = db.query(models.Courses).filter(models.Courses.Course_name_alias == request.course).first()
    new_student = models.Students(
                    id = request.unique_id, name = request.name,\
                    email = request.email, parent_name = request.parent_name,\
                    parent_number = request.parent_number,\
                    parent_number_alt = request.number, course = request.course,\
                    year = request.year,\
                    department = department.Department
                )

    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return res


def delete_student(request: Schemas.DeleteStudent, db: Session):
    # req = Schemas.TerminalZone(action = 'nothing', course = request.course, year = request.year)
    # res = attendence.remove_students(request=request, 
    #                                  save_monthly=True, 
    #                                  open_monthly=True,
    #                                  db = db)
                                     
    student = db.query(models.Students).filter(and_(
                                                models.Students.unique_id == request.unique_id,\
                                                models.Students.year == request.year,
                                                models.Students.course == request.course
                                            ))

    if not student.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Alert No User in database") 

    student.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=204)


def edit_verify_student(request: Schemas.DeleteStudent, db: Session):
    # print(request)
    student = db.query(models.Students).filter(
                and_(
                    models.Students.unique_id == request.unique_id,
                    models.Students.course == request.course,
                    models.Students.year == request.year
                )).first()

    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Alert No User in database") 

    response = Schemas.Student_v2_0(unique_id = student.unique_id, 
                                    reg_number = student.reg_number,
                                    name = student.name, 
                                    gender = student.gender,
                                    state = student.state, 
                                    parent_phone = student.parent_phone,
                                    religion = student.religion,
                                    social_status = student.social_status,
                                    year = student.year, 
                                    course = student.course
                                )

    return response


def edit_student(request: Schemas.EditStudent, db: Session):
    student = db.query(models.Students).filter(
                    and_(
                        models.Students.unique_id == request.old_unique_id,
                        # models.Students.name == request.old_name,
                        models.Students.course == request.old_course,
                        models.Students.year == request.old_year)
                    )

    if not student.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not Found")
    
    updated_details = Schemas.Student_v2_0(**request.dict())

    student.update(updated_details.dict())
    
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)