from fastapi import APIRouter
from sqlalchemy.orm.session import Session
from starlette.requests import Request
from repository import hod, Schemas
from database import database
from templates import TeacherTemplates

router = APIRouter(tags = ['Teachers'], prefix='/teacher')

get_db = database.get_db


@router.get("/add-students")
async def add_student(request: Request):
    return TeacherTemplates.addStudents(request)

@router.get("/take-attendence")
async def take_attendence(request: Request):
    return TeacherTemplates.takeAttendence(request)




