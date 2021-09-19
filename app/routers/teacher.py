from fastapi import APIRouter, Depends, Request, Response, status
from sqlalchemy.orm.session import Session
from repository import Schemas, teacher
from database import database
from templates import TeacherTemplates

router = APIRouter(tags = ['Teachers'], prefix='/teacher')

get_db = database.get_db

# teacher

@router.get("/messages/{new_five}")
async def get_messages(request: Request, db: Session = Depends(get_db),
                         new_five: bool = True):
    return TeacherTemplates.get_messages(request, db, new_five)

# templates

@router.get("/add-students")
async def add_students(request: Request):
    return TeacherTemplates.addStudents(request)

@router.get("/take-attendence")
async def take_attendence(request: Request):
    return TeacherTemplates.takeAttendence(request)

@router.get("/workspace")
async def workspace(request: Request, db: Session = Depends(get_db)):
    return TeacherTemplates.workspace(request, db)

@router.get("/message", status_code=status.HTTP_200_OK)
async def message(request: Request, db: Session = Depends(get_db)):
    return TeacherTemplates.message(request, db)

@router.get("/timetable")
async def timetable(request: Request, db: Session = Depends(get_db)):
    return TeacherTemplates.timetable(request, db)
# Students

@router.post("/add-students", status_code=status.HTTP_204_NO_CONTENT)
async def add_student(request: Schemas.AddStudent, db: Session = Depends(get_db)):
    return teacher.add_student(request, db)

@router.delete("/delete-student", status_code=status.HTTP_204_NO_CONTENT)
async def delete_student(request: Schemas.DeleteStudent, db: Session = Depends(get_db)):
    return teacher.delete_student(request, db)

@router.post("/edit-student", response_model=Schemas.AddStudent)
async def edit_verify_student(request: Schemas.DeleteStudent, db: Session = Depends(get_db)):
    return teacher.edit_verify_student(request, db)

@router.put("/edit-student", status_code=status.HTTP_204_NO_CONTENT)
async def edit_student(request: Schemas.EditStudent, db: Session = Depends(get_db)):
    return teacher.edit_student(request, db)