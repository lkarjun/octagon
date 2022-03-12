from database.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean
from sqlalchemy.orm import relationship

# ======================================V2.0=========================================================
# Changes needed here

class Hod(Base):
    __tablename__ = "Department Heads"
    id = Column(String, primary_key=True, index=True)
    name = Column(String)
    username = Column(String)
    email = Column(String)
    phone_num = Column(Integer)
    department = Column(String)
    tag = Column(String)
    joining_date = Column(String)
    dob = Column(String)
    higher_qualification = Column(String)
    net_qualification  = Column(String)
    designation = Column(String)
    gender = Column(String)
    teaching_experience = Column(String)
    religion = Column(String)
    social_status = Column(String)
    status = Column(String, default="status")
    discontinued_date = Column(String, default="-")

class Teachers(Base):
    __tablename__ = "Teacher"
    id = Column(String, primary_key=True, index=True)
    name = Column(String)
    username = Column(String)
    email = Column(String)
    phone_num = Column(Integer)
    department = Column(String)
    tag = Column(String)
    joining_date = Column(String)
    dob = Column(String)
    higher_qualification = Column(String)
    net_qualification  = Column(String)
    designation = Column(String)
    gender = Column(String)
    teaching_experience = Column(String)
    religion = Column(String)
    social_status = Column(String)
    status = Column(String, default="status")
    discontinued_date = Column(String, default="-")

class Students(Base):
    __tablename__ = 'Students'
    unique_id = Column(String, primary_key=True)
    reg_number = Column(String)
    name = Column(String)
    gender = Column(String)
    state = Column(String)
    parent_phone = Column(Integer)
    religion = Column(String)
    social_status = Column(String)
    status = Column(String)
    course = Column(String)
    year = Column(Integer)
    department = Column(String)
    discontinued_date = Column(String, default="-")

# ======================================V2.0=========================================================

# class HOD(Base):
#     __tablename__ = 'Hod'
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String)
#     email = Column(String)
#     phone_num = Column(String)
#     username = Column(String)
#     department = Column(String)

class Admin(Base):
    __tablename__ = 'Admin'
    name = Column(String, primary_key=True, index=True)
    password = Column(String)

class Departments(Base):
    __tablename__ = 'Departments'
    Department = Column(String, primary_key=True, index=True, nullable=False)
    Alias = Column(String)

class Courses(Base):
    __tablename__ = 'Courses'
    Course_name = Column(String, primary_key=True, index=True)
    Course_name_alias = Column(String)
    Duration = Column(Integer)
    Department = Column(String)

# class TEACHERS(Base):
#     __tablename__ = 'Teachers_OL'
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, nullable=False)
#     username = Column(String, unique=True)
#     department = Column(String, nullable=False)
#     email = Column(String, unique=True, nullable=False)
#     phone_num = Column(String, nullable=True)
#     tag = Column(String)

class Timetable(Base):
    __tablename__ = 'Timetables'
    id = Column(Integer, primary_key=True, index=True)
    department = Column(String)
    course = Column(String)
    year = Column(Integer)
    days = Column(String)
    hour_1 = Column(String)
    hour_2 = Column(String)
    hour_3 = Column(String)
    hour_4 = Column(String)
    hour_5 = Column(String)

class TimetableS(Base):
    __tablename__ = "TimeTableSubjects"
    id = Column(Integer, primary_key=True, index=True)
    department = Column(String)
    course = Column(String)
    year = Column(Integer)
    days = Column(String)
    hour_1 = Column(String)
    hour_2 = Column(String)
    hour_3 = Column(String)
    hour_4 = Column(String)
    hour_5 = Column(String)

# class STUDENTS(Base):
#     __tablename__ = 'Students_Ol'
#     id = Column(String, primary_key=True)
#     name = Column(String)
#     email = Column(String)
#     parent_name = Column(String)
#     parent_number = Column(Integer)
#     parent_number_alt = Column(Integer)
#     course = Column(String)
#     year = Column(Integer)
#     department = Column(String)

class Corrections(Base):
    __tablename__ = "Attendence Correction"
    id = Column(Integer, primary_key=True, index=True)
    course = Column(String)
    year = Column(String)
    date = Column(String)
    student_name = Column(String)
    reason = Column(String)
    percentage = Column(Float)

class Message(Base):
    __tablename__ = "Messages"
    id = Column(Integer, primary_key=True, index=True)
    hod_name = Column(String)
    hod_department = Column(String)
    date = Column(String)
    to = Column(String)
    title = Column(String)
    message = Column(String)
    important = Column(Boolean)


class PendingVerificationImage(Base):
    __tablename__ = "PendingVerification"
    id = Column(String, primary_key=True)
    user_username = Column(String)
    user_email = Column(String)
    hod_or_teacher = Column(String)