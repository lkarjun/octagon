from fastapi import APIRouter, Depends, Request, Response, status
from sqlalchemy.orm.session import Session
from repository import Schemas, teacher
from database import database
from templates import TeacherTemplates

router = APIRouter(tags = ['Teachers'], prefix='/teacher')

get_db = database.get_db


# templates

@router.get("/add-students")
async def add_students(request: Request):
    return TeacherTemplates.addStudents(request)

@router.get("/take-attendence")
async def take_attendence(request: Request):
    return TeacherTemplates.takeAttendence(request)

@router.get("/workspace")
async def workspace(request: Request):
    return TeacherTemplates.workspace(request)

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