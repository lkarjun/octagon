from pydantic import BaseModel
from typing import Optional

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

