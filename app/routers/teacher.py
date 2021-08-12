from fastapi import APIRouter, Depends, Request, Response, status
from sqlalchemy.orm.session import Session
from repository import hod, Schemas
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


# functions

@router.post("/add-students", status_code=status.HTTP_204_NO_CONTENT)
async def add_student(request: Schemas.AddStudent, db: Session = Depends(get_db)):
    print(request)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.delete("/delete-student")
async def delete_student(request: Schemas.DeleteStudent, db: Session = Depends(get_db)):
    print(request)
    return True

@router.post("/edit-student", response_model=Schemas.AddStudent)
async def edit_student(request: Schemas.DeleteStudent, db: Session = Depends(get_db)):
    print(request)

    res = Schemas.AddStudent(unique_id = "idtest", name = "arjun" ,email = "adfkl@gmail.com",
                                parent_name = "Lal", parent_number = 23232, number = 23232, 
                                course = "None", year = 2)

    return res