from os import stat
from fastapi import (APIRouter, Depends, Request, 
                    Response, status, UploadFile, 
                    File, Form, HTTPException)
from sqlalchemy.orm.session import Session
from repository import Schemas, teacher
from database import database
from templates import TeacherTemplates
from security import oauth2, faceid

router = APIRouter(tags = ['Teachers'], prefix='/teacher')

get_db = database.get_db

# teacher

@router.get("/messages/{new_five}")
async def get_messages(request: Request, db: Session = Depends(get_db),
                         new_five: bool = True, user=Depends(oauth2.manager_teacher)):
    return TeacherTemplates.get_messages(request, db, new_five, user)

@router.post('/verification_image', status_code=status.HTTP_204_NO_CONTENT)
async def verification_image(username: str = Form(...),
                             image1: UploadFile = File(...),
                             image2: UploadFile = File(...),
                             image3: UploadFile = File(...),
                             user=Depends(oauth2.manager_hod)):
    image1, image2, image3 = await image1.read(), await image2.read(),\
                                await image3.read()
    return faceid.verification_image(username, image1, image2, image3)

# templates

@router.get("/add-students")
async def add_students(request: Request, 
                       db: Session = Depends(get_db),
                       user=Depends(oauth2.manager_teacher)):
    return TeacherTemplates.addStudents(request, user, db)

@router.get("/take-attendence")
async def take_attendence(request: Request, user=Depends(oauth2.manager_teacher)):
    return TeacherTemplates.takeAttendence(request)

@router.get("/workspace")
async def workspace(request: Request, db: Session = Depends(get_db),
                        user=Depends(oauth2.manager_teacher)):
    return TeacherTemplates.workspace(request, db, user)

@router.get("/message", status_code=status.HTTP_200_OK)
async def message(request: Request, db: Session = Depends(get_db),
                    user=Depends(oauth2.manager_teacher)):
    return TeacherTemplates.message(request, db, user)

@router.get("/timetable")
async def timetable(request: Request, db: Session = Depends(get_db),
                    user=Depends(oauth2.manager_teacher)):
    return TeacherTemplates.timetable(request, db, user)

@router.get("/profile")
async def profile(request: Request, user=Depends(oauth2.manager_teacher)):
    return TeacherTemplates.profile(request, user)

@router.put("/update_profile", status_code=status.HTTP_204_NO_CONTENT)
async def update_user_profile(data: Schemas.Staff_v2_0, 
                              user=Depends(oauth2.manager_teacher),
                              db: Session = Depends(get_db)):
    return teacher.update_profile(data, db, user)

# Students

@router.get("/students")
async def students_details_(request: Request, 
                            db: Session = Depends(get_db),
                            user=Depends(oauth2.manager_teacher)):
    return TeacherTemplates.students(request, db, user)

@router.get("/students-attendence/details/{course}/{year}", status_code=status.HTTP_200_OK)
async def student_details(request: Request, course: str, year: int,
                          db: Session = Depends(get_db),
                          user=Depends(oauth2.manager_teacher)
                        ):
    return TeacherTemplates.show_student_details(request, course, year, db)

@router.post("/add-students", status_code=status.HTTP_204_NO_CONTENT)
async def add_student(request: Schemas.AddStudent, db: Session = Depends(get_db),
                                ):
    return teacher.add_student(request, db)

@router.post("/add-students-v2-0", status_code=status.HTTP_204_NO_CONTENT)
async def add_student_v2_0(request: Schemas.Student_v2_0,
                           db: Session = Depends(get_db),
                         ):
    teacher.add_student_v2_0(request, db)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# =================================================================================================
# Changes needed here
@router.post("/add-students-from-file", status_code=status.HTTP_204_NO_CONTENT)
async def add_students_from_file(
                                course: str = Form(...),
                                year: int = Form(...),
                                DATA: UploadFile = File(...),
                                ):
    if DATA.content_type not in ['text/csv', 'text/xlxm', 'text/xls']:
        raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# =================================================================================================

@router.delete("/delete-student", status_code=status.HTTP_204_NO_CONTENT)
async def delete_student(request: Schemas.DeleteStudent, db: Session = Depends(get_db)):
    return teacher.delete_student(request, db)

@router.post("/edit-student", response_model=Schemas.AddStudent)
async def edit_verify_student(request: Schemas.DeleteStudent, db: Session = Depends(get_db)):
    return teacher.edit_verify_student(request, db)

@router.put("/edit-student", status_code=status.HTTP_204_NO_CONTENT)
async def edit_student(request: Schemas.EditStudent, db: Session = Depends(get_db),
                        ):
    return teacher.edit_student(request, db)