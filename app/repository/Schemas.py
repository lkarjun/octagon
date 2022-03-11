from pydantic import BaseModel
from typing import Optional, List, Union
from pathlib import Path
from pandas import DataFrame



#==========================Changing v2.0=============================

class AdmitStudentFromFile_v2_0(BaseModel):
    file: DataFrame
    course: str
    year: int

    class Config:
        arbitrary_types_allowed = True

class Student_v2_0(BaseModel):
    reg_no: str
    # or unique_id
    name: str
    parent_number: str
    course: str
    year: int


class Staff_v2_0(BaseModel):
    id: str
    name: str
    username: str
    email: str
    phone_num: int
    department: str
    tag: str
    joining_date: str
    dob: str
    higher_qualification: str
    net_qualification: str
    designation: str
    gender: str
    teaching_experience: int #year of teaching other than current
    religion: str
    social_status: str
    status: str = "Continue"
    discontinued_date: str = "-"


class Student_v2_0(BaseModel):
    unique_id: str
    reg_number: str = "None"
    name: str
    gender: str
    state: str
    parent_phone: int
    religion: str
    social_status: str
    status: str = "Continue"
    course: str
    year: int = 1

class StudentsAttendence_v2_0(BaseModel): 
    datas: List
    # ids: List[str]
    # names: List[str]

class TakeAttendence_v2_0(BaseModel):
    course: str
    year: int
    take_full_day: bool
    date: str
    present: List[str]

class Staff_v2_0_status(BaseModel):
    username: str
    status: str
#====================================================================


class CreateHod(BaseModel):
    name: str
    email: str
    phone_num: int
    username: str
    department: str

class ShowHods(CreateHod):
    class Config():
        orm_mode = True

class DeleteHod(BaseModel):
    username: str

class PendingVerification(BaseModel):
    username: str

class AddDepartment(BaseModel):
    Department: str
    Alias: str

class AddCourse(BaseModel):
    course_name: str
    course_alias: str
    duration: int
    department: str

class DeleteDepartment(BaseModel):
    department: str

class DeleteCourse(BaseModel):
    course_name: str

class AdminPass(BaseModel):
    username: str = 'Admin'
    current_pass: str
    new_pass: str

class Admin(BaseModel):
    username: str

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    admin: Optional[str] = None


class TerminalZone(BaseModel):
    action: str
    course: str
    year: int

class AddTeacher(BaseModel):
    name: str
    username: str
    department: str
    email: str
    phone_num: int
    tag: str

class ShowTeacher(AddTeacher):
    class Config():
        orm_mode = True

class DeleteTeacher(BaseModel):
    name: str
    username: str

class TimeTable(BaseModel):
    department: str
    course: str
    days: List[str] = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    year: int
    day_1: List[str]
    day_2: List[str]
    day_3: List[str]
    day_4: List[str]
    day_5: List[str]
    sub_day_1: List
    sub_day_2: List
    sub_day_3: List
    sub_day_4: List
    sub_day_5: List

class TimeTableChecker(BaseModel):
    day: str 
    name: str
    hour: str

class TimeTableEdit(BaseModel):
    course: str
    year: int
    department: str

class CurrentHour(BaseModel):
    name: str
    course: str
    year: str
    hour: str


class AddStudent(BaseModel):
    unique_id: str
    name: str
    email: str
    parent_name: str
    parent_number: int
    number: int
    course: str
    year: int

class EditStudent(AddStudent):
    old_unique_id: str
    old_name: str
    old_course: str
    old_year: int

class DeleteStudent(BaseModel):
    unique_id: str
    name: str
    course: str
    year: int



# Attendence
class students_attendence(BaseModel): 
    names: List[str]

class set_class(BaseModel):
    course: str
    year: int
    date: str

class Files(BaseModel):
    daily: Union[None, DataFrame]
    monthly: Union[None, DataFrame]
    daily_path: Path
    monthly_path: Path
    
    class Config:
        arbitrary_types_allowed = True

class TakeAttendence(BaseModel):
    course: str
    year: int
    take_full_day: bool
    date: str
    present: List[str]

class Analysing(BaseModel):
    course: str
    year: int
    last_month: bool
    which_month: Optional[str] = None

class ShowAttendence(BaseModel):
    course: str
    year: int

class MostAbsentee(BaseModel):
    course: str
    year: int

class AttendenceCorrection(BaseModel):
    names: List[str]
    date: str
    percentage: float
    reason: str
    course: str
    year: int

class Message(BaseModel):
    title: str
    message: str
    to: str
    important: bool
    date: str

class HourDetails(BaseModel):
    course: str
    hour: int
    year: int