from fastapi import APIRouter, Request, Depends, status, Form, UploadFile, File, BackgroundTasks, HTTPException
from sqlalchemy.orm.session import Session
from starlette.responses import HTMLResponse, Response
from repository import hod, Schemas, attendence, admin
from database import database
from templates import HodTemplates
from typing import Dict, List
from security import oauth2, faceid

router = APIRouter(tags = ['Head Of Department'], prefix='/hod')

get_db = database.get_db


# Teacher Related
#================================v2.0===========================================
@router.post("/Addteacher_v2_0", status_code = status.HTTP_204_NO_CONTENT)
async def appoint_teacher(data: Schemas.Staff_v2_0, 
                      bg_task: BackgroundTasks,
                      db: Session = Depends(get_db),
                      user = Depends(oauth2.manager_hod)):
    return hod.appoint_teacher_v2_0(data, db, bg_task)

@router.put("/change_status", status_code=status.HTTP_204_NO_CONTENT)
async def change_status(request: Schemas.Staff_v2_0_status, db: Session = Depends(get_db),\
            user=Depends(oauth2.manager_hod)):
        return hod.change_status(request, db)
#==============================================================================

@router.post('/Addteacher', status_code=status.HTTP_204_NO_CONTENT)
async def add_teacher(request: Schemas.AddTeacher, 
                      bg_task: BackgroundTasks,
                      db: Session = Depends(get_db),
                      user=Depends(oauth2.manager_hod)):
    return hod.appoint_teacher(request, db, bg_task)

@router.delete('/Deleteteacher', status_code=status.HTTP_204_NO_CONTENT)
async def delete_teacher(request: Schemas.DeleteTeacher, 
            db: Session = Depends(get_db), user=Depends(oauth2.manager_hod)):
    return hod.remove_teacher(request, db)

@router.put('/Updateteacher', status_code=status.HTTP_202_ACCEPTED)
async def update_teacher(email: str, request: Schemas.AddTeacher,
             db: Session = Depends(get_db), user=Depends(oauth2.manager_hod)):
    return hod.update(email, request, db)

@router.get('/Teachersdetail', status_code=status.HTTP_202_ACCEPTED, response_model=List[Schemas.ShowTeacher])
async def teachers_detail(db: Session = Depends(get_db),user=Depends(oauth2.manager_hod)):
    return hod.get_techer_details(db)

@router.post('/verification_image', status_code=status.HTTP_204_NO_CONTENT)
async def verification_image(username: str = Form(...),
                            image1: UploadFile = File(...),
                            image2: UploadFile = File(...),
                            image3: UploadFile = File(...),
                            user=Depends(oauth2.manager_hod)):
    image1, image2, image3 = await image1.read(), await image2.read(),\
                                await image3.read()
    return faceid.verification_image(username, image1, image2, image3)

# Students Related

@router.post("/students-attendence/corrections", status_code=status.HTTP_204_NO_CONTENT)
async def attendence_correction(request: Schemas.AttendenceCorrection, 
            db: Session = Depends(get_db), user=Depends(oauth2.manager_hod)):
    return attendence.attendence_correction(request=request, db=db)


# Hod Functions

@router.get("/myclasses")
async def timetable(request: Request, db: Session = Depends(get_db),
                    user=Depends(oauth2.manager_hod)):
    return HodTemplates.myclasses(request, db, user)

@router.post('/message', status_code=status.HTTP_204_NO_CONTENT)
async def message(request: Schemas.Message, db: Session = Depends(get_db),
            user=Depends(oauth2.manager_hod)):
    return hod.send_message(user, request, db)

@router.post('/CreateTimeTable', status_code=status.HTTP_201_CREATED)
async def create_time_table(request: Schemas.TimeTable, db: Session = Depends(get_db),
            user=Depends(oauth2.manager_hod)):
    return hod.set_timetable(request, db)

@router.post('/check_teacher', status_code=status.HTTP_202_ACCEPTED)
async def check_teacher_allocation(request: Schemas.TimeTableChecker,
            db: Session = Depends(get_db), user=Depends(oauth2.manager_hod)):
    return hod.check_timetable(request, db)

@router.post('/display_timetable')
async def display_timetable(request: Schemas.TimeTableEdit, db: Session = Depends(get_db),
                    user=Depends(oauth2.manager_hod)):
    return hod.display_timetable(request, db)

@router.delete('/delete_timetable', status_code=status.HTTP_204_NO_CONTENT)
async def remove_timetable(request: Schemas.TimeTableEdit, db: Session = Depends(get_db),
                    user=Depends(oauth2.manager_hod)):
    return hod.remove_timetable(request, db)

@router.get('/CurrentHour', response_model=List[Schemas.CurrentHour], status_code=status.HTTP_202_ACCEPTED)
async def get_current_hour_detail(department: str, day: str, hour: str, 
                    db: Session = Depends(get_db), user=Depends(oauth2.manager_hod)):
    return hod.current_hour_detail(department, day, hour, db)

@router.get("/full_message")
async def get_full_message(request: Request, db: Session = Depends(get_db), user=Depends(oauth2.manager_hod)):
    return HodTemplates.get_full_messages(request, db, user)

@router.post("/clear_messages")
async def clear_message(db: Session = Depends(get_db), user=Depends(oauth2.manager_hod)):
    return hod.clear_message(db, user)


@router.post("/update_profile")
async def update_profile(data: Schemas.Staff_v2_0, db: Session = Depends(get_db), 
                user=Depends(oauth2.manager_hod)):
    return hod.update_profile(data, db, user)


@router.post("/terminalzone")
async def terminalzone(request: Schemas.TerminalZone, db: Session = Depends(get_db),
                       user=Depends(oauth2.manager_hod)):
    return hod.terminalzone(request, db, user)


# =================================================================================================
# Changes needed here
@router.post("/add-teacher-from-file", status_code=status.HTTP_204_NO_CONTENT)
async def add_hod_from_file(
                            bg_task: BackgroundTasks,
                            department: str = Form(...),
                            DATA: UploadFile = File(...),
                            db: Session = Depends(get_db)

                            ):
    if DATA.content_type not in ['text/csv', 'text/xlxm', 'text/xls']:
        raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
    return hod.appoint_teacher_v2_0_from_file(DATA, department, db, bg_task)

# =================================================================================================

# Pages
@router.get("/workspace")
async def workspace(request: Request, db: Session = Depends(get_db),
                            user=Depends(oauth2.manager_hod)):
    return HodTemplates.workspace(request, user, db)

@router.get("/message")
async def message(request: Request, user=Depends(oauth2.manager_hod)):
    return HodTemplates.message(request)

@router.get('/uoc-notification',)
async def uoc_notificaions(request: Request, user=Depends(oauth2.manager_hod)):
    return HodTemplates.uoc_notification(request)

@router.get('/exam-notification')
async def uoc_exam_notificaions(request: Request, user=Depends(oauth2.manager_hod)):
    return HodTemplates.exam_notification(request)

@router.get('/students-attendence')
async def attendenceDataView(request: Request, user=Depends(oauth2.manager_hod)):
    return HodTemplates.attendenceDataView(request, user)

@router.get("/take-attendence")
async def take_attendence(request: Request, user=Depends(oauth2.manager_hod)):
    return HodTemplates.takeAttendence(request)

@router.get('/timetable')
async def timetable(request: Request, user=Depends(oauth2.manager_hod),
                    db: Session = Depends(get_db)):
    return HodTemplates.timetable(request, user, db)

@router.get("/edit-teacher")
async def appoint_teacher(request: Request,user=Depends(oauth2.manager_hod)):
    return HodTemplates.appoint_teacher(request, user)

@router.get("/mydepartment")
async def appoint_teacher(request: Request,
                          user=Depends(oauth2.manager_hod),
                          db: Session = Depends(get_db)):
    return HodTemplates.manage_department(request, user, db)

@router.post("/check_st_detail", status_code=status.HTTP_204_NO_CONTENT)
async def check_st_detail(request: Schemas.TerminalZone, db: Session = Depends(get_db)):
    return hod.check_st_details(request, db)

@router.get("/students-attendence/{course}/{year}", status_code=status.HTTP_200_OK)
async def show_attendence(request: Request, course: str, year: int,
                user=Depends(oauth2.manager_hod)):
    data = Schemas.ShowAttendence(course=course, year = year)
    return HodTemplates.show_attendence_data(request, data)

@router.post("/get_attendence_data")
async def get_attendence_data(data: Schemas.ShowAttendence):
    import time;time.sleep(1)
    # column, values = attendence.show_attendence_data(request=data)
    return HodTemplates.get_attendence_data(data)

@router.get("/students-attendence/details/{course}/{year}", status_code=status.HTTP_200_OK)
async def student_details(request: Request, course: str, year: int,
                user=Depends(oauth2.manager_hod)):
    return HodTemplates.show_student_details(request, course, year)

@router.post("/most_absentee", status_code=status.HTTP_200_OK)
async def most_absentee(request: Request, data: Schemas.MostAbsentee,
                user=Depends(oauth2.manager_hod)):
    return HodTemplates.show_most_absentees(request, data)

@router.post("/get_students_name_and_id")
async def get_students_name_and_id(request: Schemas.get_names):
    return attendence.get_student_names_for_status_update(data = request)

@router.post("/change_student_status")
async def update_students_status(request: Schemas.Students_status_update, db: Session = Depends(get_db)):
    return hod.update_students_status(request, db)
    print(request)
    return Response(status_code=204)

@router.post("/get_report")
async def get_report(request: Request, data: Schemas.Analysing,
                user=Depends(oauth2.manager_hod)):
    return HodTemplates.show_report(request, data)

@router.get("/latest_notification")
async def get_notification(request: Request, which_notification: str,
                user=Depends(oauth2.manager_hod)):
    return HodTemplates.latest_notfications(request, which_notification)

@router.get("/profile")
async def profile(request: Request, user = Depends(oauth2.manager_hod)):
    return HodTemplates.profile(request, user)

@router.get("/students")
async def students(request: Request, 
                   user=Depends(oauth2.manager_hod),
                   db: Session = Depends(get_db)):
    return HodTemplates.students(request, user, db)

@router.get("/add-students")
async def add_student(request: Request,
                      user = Depends(oauth2.manager_hod),
                      db: Session = Depends(get_db)
                    ):

    return HodTemplates.addStudents(request, user, db)

@router.get("/search-students")
async def search_students(request: Request,
                          user = Depends(oauth2.manager_hod),
                          db: Session = Depends(get_db)):
    return HodTemplates.search_students(request, user, db)