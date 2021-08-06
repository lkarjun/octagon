from fastapi import APIRouter, Request, Depends, status
from sqlalchemy.orm.session import Session
from repository import hod, Schemas
from database import database
from templates import HodTemplates
from typing import List

router = APIRouter(tags = ['Head Of Department'], prefix='/hod')

get_db = database.get_db


# Teacher Related
@router.get('/timetable')
async def timetable(request: Request):
    return HodTemplates.timetable(request)

@router.get("/edit-teacher")
async def appoint_teacher(request: Request):
    return HodTemplates.appoint_teacher(request)

@router.post('/Addteacher', status_code=status.HTTP_201_CREATED, response_model=Schemas.ShowTeacher)
async def add_teacher(request: Schemas.AddTeacher, db: Session = Depends(get_db)):
    return hod.create(request, db)

@router.delete('/Deleteteacher', status_code=status.HTTP_204_NO_CONTENT)
async def delete_teacher(request: Schemas.DeleteTeacher, db: Session = Depends(get_db)):
    return hod.delete(request, db)

@router.put('/Updateteacher', status_code=status.HTTP_202_ACCEPTED)
async def update_teacher(email: str, request: Schemas.AddTeacher, db: Session = Depends(get_db)):
    return hod.update(email, request, db)

@router.get('/Teachersdetail', status_code=status.HTTP_202_ACCEPTED, response_model=List[Schemas.ShowTeacher])
async def teachers_detail(db: Session = Depends(get_db)):
    return hod.get_techer_details(db)


# Students Related

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

@router.get('/uoc-notification')
async def uoc_notificaions(request: Request):
    return HodTemplates.uoc_notification(request)

@router.get('/students-attendence')
async def attendenceDataView(request: Request):
    return HodTemplates.attendenceDataView(request)