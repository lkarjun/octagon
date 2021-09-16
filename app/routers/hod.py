from fastapi import APIRouter, Request, Depends, status, Form, UploadFile, File
from sqlalchemy.orm.session import Session
from starlette.responses import HTMLResponse, Response
from repository import hod, Schemas, attendence
from database import database
from templates import HodTemplates
from typing import List

router = APIRouter(tags = ['Head Of Department'], prefix='/hod')

get_db = database.get_db


# Teacher Related

@router.post('/Addteacher', status_code=status.HTTP_204_NO_CONTENT)
async def add_teacher(request: Schemas.AddTeacher, db: Session = Depends(get_db)):
    return hod.appoint_teacher(request, db)

@router.delete('/Deleteteacher', status_code=status.HTTP_204_NO_CONTENT)
async def delete_teacher(request: Schemas.DeleteTeacher, db: Session = Depends(get_db)):
    return hod.remove_teacher(request, db)

@router.put('/Updateteacher', status_code=status.HTTP_202_ACCEPTED)
async def update_teacher(email: str, request: Schemas.AddTeacher, db: Session = Depends(get_db)):
    return hod.update(email, request, db)

@router.get('/Teachersdetail', status_code=status.HTTP_202_ACCEPTED, response_model=List[Schemas.ShowTeacher])
async def teachers_detail(db: Session = Depends(get_db)):
    return hod.get_techer_details(db)

@router.post('/verification_image', status_code=status.HTTP_204_NO_CONTENT)
async def verification_image(username: str = Form(...),
                            image1: UploadFile = File(...),
                            image2: UploadFile = File(...),
                            image3: UploadFile = File(...)):
    print(image1.filename, username)
    return Response(status_code=204)

# Students Related

@router.post("/students-attendence/corrections", status_code=status.HTTP_204_NO_CONTENT)
async def attendence_correction(request: Schemas.AttendenceCorrection, db: Session = Depends(get_db)):
    return attendence.attendence_correction(request=request, db=db)

# @router.post('/StudentsAttendence')
# async def take_studentattendence(request: Request):...

# @router.get('/AttendenceReport')
# async def get_attendence_report(request: Request):...

# # Annousement for teachers
# @router.post('/MessageTeacher')
# async def send_message_teacher(request: Request):...

# Hod Functions

@router.post('/Message/{who}', status_code=status.HTTP_200_OK)
async def mail(who: str, message: str, db: Session = Depends(get_db)):
    return hod.mail_(who, message, db)

@router.post('/CreateTimeTable', status_code=status.HTTP_201_CREATED)
async def create_time_table(request: Schemas.TimeTable, db: Session = Depends(get_db)):
    return hod.set_timetable(request, db)

@router.post('/check_teacher', status_code=status.HTTP_202_ACCEPTED)
async def check_teacher_allocation(request: Schemas.TimeTableChecker, db: Session = Depends(get_db)):
    return hod.check_timetable(request, db)

@router.post('/display_timetable')
async def display_timetable(request: Schemas.TimeTableEdit, db: Session = Depends(get_db)):
    return hod.display_timetable(request, db)

@router.delete('/delete_timetable', status_code=status.HTTP_204_NO_CONTENT)
async def remove_timetable(request: Schemas.TimeTableEdit, db: Session = Depends(get_db)):
    return hod.remove_timetable(request, db)

@router.get('/CurrentHour', response_model=List[Schemas.CurrentHour], status_code=status.HTTP_202_ACCEPTED)
async def get_current_hour_detail(department: str, day: str, hour: str, db: Session = Depends(get_db)):
    return hod.current_hour_detail(department, day, hour, db)


# Pages
@router.get("/workspace")
async def workspace(request: Request):
    return HodTemplates.workspace(request)

@router.get('/uoc-notification')
async def uoc_notificaions(request: Request):
    return HodTemplates.uoc_notification(request)

@router.get('/exam-notification')
async def uoc_exam_notificaions(request: Request):
    return HodTemplates.exam_notification(request)

@router.get('/students-attendence')
async def attendenceDataView(request: Request):
    return HodTemplates.attendenceDataView(request)

@router.get("/take-attendence")
async def take_attendence(request: Request):
    return HodTemplates.takeAttendence(request)

@router.get('/timetable')
async def timetable(request: Request):
    return HodTemplates.timetable(request)

@router.get("/edit-teacher")
async def appoint_teacher(request: Request):
    return HodTemplates.appoint_teacher(request)

@router.get("/students-attendence/{course}/{year}", status_code=status.HTTP_200_OK)
async def show_attendence(request: Request, course: str, year: int):
    data = Schemas.ShowAttendence(course=course, year = year)
    return HodTemplates.show_attendence_data(request, data)

@router.get("/students-attendence/details/{course}/{year}", status_code=status.HTTP_200_OK)
async def student_details(request: Request, course: str, year: int):
    return HodTemplates.show_student_details(request, course, year)

@router.post("/most_absentee", status_code=status.HTTP_200_OK)
async def most_absentee(request: Request, data: Schemas.MostAbsentee):
    return HodTemplates.show_most_absentees(request, data)

@router.post("/get_report")
async def get_report(request: Request, data: Schemas.Analysing):
    return HodTemplates.show_report(request, data)

@router.get("/latest_notification")
async def get_notification(request: Request, which_notification: str):
    return HodTemplates.latest_notfications(request, which_notification)