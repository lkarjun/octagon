from models import Courses
from pydantic import BaseModel
from typing import Optional, List

class CreateHod(BaseModel):
    name: str
    email: str
    phone_num: int
    user_name: str
    department: str

class ShowHods(CreateHod):
    class Config():
        orm_mode = True

class AddDepartment(BaseModel):
    Department: str
    Alias: str

class AddCourse(BaseModel):
    course_name: str
    course_alias: str
    duration: int
    department: str

class DeleteCourse(BaseModel):
    course_name: str
    department: str

class AdminPass(BaseModel):
    username: str
    current_pass: str
    new_pass: str

class Admin(BaseModel):
    username: str

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    admin: Optional[str] = None


class AddTeacher(BaseModel):
    name: str
    department: str
    email: str
    phone_number: Optional[int]

class ShowTeacher(AddTeacher):
    class Config():
        orm_mode = True

class TimeTable(BaseModel):
    department: Optional[str]
    course: str
    days: List[str] = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    year: int
    day_1: Optional[List[str]]
    day_2: Optional[List[str]]
    day_3: Optional[List[str]]
    day_4: Optional[List[str]]
    day_5: Optional[List[str]]

class TimeTableChecker(BaseModel):
    day: str 
    name: str
    hour: str

class CurrentHour(BaseModel):
    name: str
    course: str
    year: str
    hour: str