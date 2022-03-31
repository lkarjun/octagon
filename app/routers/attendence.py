from fastapi import APIRouter, Depends, Request, Response, status
from sqlalchemy.orm.session import Session
from repository import Schemas, attendence
from database import database

# common
router = APIRouter(tags = ['Attendence'], prefix='/attendence')

# get_db = database.get_db


@router.post("/set_class", response_model=Schemas.StudentsAttendence_v2_0)
async def get_student_names(request: Schemas.set_class):
    res = attendence.get_student_names(data=request)
    return res

@router.post("/take-attendence", status_code=status.HTTP_204_NO_CONTENT)
async def take_attendence(data: Schemas.TakeAttendence_v2_0):
    return attendence.take_attendence(data=data)