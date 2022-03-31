from database.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, UniqueConstraint
from sqlalchemy.orm import relationship

# ======================================V2.0=========================================================
# Changes needed here

class Hod(Base):
    __tablename__ = "Department Heads"
    id = Column(String, primary_key=True, index=True, nullable=False, unique=True)
    name = Column(String, nullable=False)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, nullable=False)
    phone_num = Column(Integer, nullable=False)
    department = Column(String, ForeignKey('Departments.Alias'), nullable=False)
    tag = Column(String, nullable=False)
    joining_date = Column(String, nullable=False)
    dob = Column(String, nullable=False)
    higher_qualification = Column(String, nullable=False)
    net_qualification  = Column(String, nullable=False)
    designation = Column(String, nullable=False)
    gender = Column(String, nullable=False)
    teaching_experience = Column(String, nullable=False)
    religion = Column(String, nullable=False)
    social_status = Column(String, nullable=False)
    status = Column(String, default="status", nullable=False)
    discontinued_date = Column(String, default="-", nullable=False)

class Teachers(Base):
    __tablename__ = "Teacher"
    id = Column(String, primary_key=True, index=True, nullable=False, unique=True)
    name = Column(String, nullable=False)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, nullable=False)
    phone_num = Column(Integer, nullable=False)
    department = Column(String, ForeignKey('Departments.Alias'), nullable=False)
    tag = Column(String, nullable=False)
    joining_date = Column(String, nullable=False)
    dob = Column(String, nullable=False)
    higher_qualification = Column(String, nullable=False)
    net_qualification  = Column(String, nullable=False)
    designation = Column(String, nullable=False)
    gender = Column(String, nullable=False)
    teaching_experience = Column(String, nullable=False)
    religion = Column(String, nullable=False)
    social_status = Column(String, nullable=False)
    status = Column(String, default="status", nullable=False)
    discontinued_date = Column(String, default="-", nullable=False)

class Students(Base):
    __tablename__ = 'Students'
    unique_id = Column(String, primary_key=True, nullable=False, unique=True)
    reg_number = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=False)
    gender = Column(String, nullable=False)
    state = Column(String, nullable=False)
    parent_phone = Column(Integer, nullable=False)
    religion = Column(String, nullable=False)
    social_status = Column(String, nullable=False)
    status = Column(String, nullable=False)
    department = Column(String, ForeignKey('Departments.Alias'), nullable=False)
    course = Column(String, ForeignKey('Courses.Course_name_alias'), nullable=False)
    year = Column(Integer, nullable=False)
    discontinued_date = Column(String, default="-", nullable=False)

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
    name = Column(String, primary_key=True, index=True, nullable=False)
    password = Column(String, nullable=False, unique=True)

class Departments(Base):
    __tablename__ = 'Departments'
    Department = Column(String, nullable=False)
    Alias = Column(String, primary_key=True, index=True, nullable=False)

class Courses(Base):
    __tablename__ = 'Courses'
    Course_name = Column(String, nullable=False)
    Course_name_alias = Column(String, primary_key=True, index=True)
    Duration = Column(Integer, nullable=False)
    Department = Column(String, ForeignKey('Departments.Alias'), nullable=False)

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
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    department = Column(String, ForeignKey('Departments.Alias'), nullable=False)
    course = Column(String, ForeignKey('Courses.Course_name_alias'), nullable=False)
    year = Column(Integer, nullable=False)
    days = Column(String, nullable=False)
    hour_1 = Column(String, nullable=False)
    hour_2 = Column(String, nullable=False)
    hour_3 = Column(String, nullable=False)
    hour_4 = Column(String, nullable=False)
    hour_5 = Column(String, nullable=False)

class TimetableS(Base):
    __tablename__ = "TimeTableSubjects"
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    department = Column(String, ForeignKey('Departments.Alias'), nullable=False)
    course = Column(String, ForeignKey('Courses.Course_name_alias'), nullable=False)
    year = Column(Integer, nullable=False)
    days = Column(String, nullable=False)
    hour_1 = Column(String, nullable=False)
    hour_2 = Column(String, nullable=False)
    hour_3 = Column(String, nullable=False)
    hour_4 = Column(String, nullable=False)
    hour_5 = Column(String, nullable=False)

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
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    course = Column(String, ForeignKey('Courses.Course_name_alias'), nullable=False)
    year = Column(String, nullable=False)
    department = Column(String, ForeignKey('Departments.Alias'), nullable=False)
    date = Column(String, nullable=False)
    student_ids = Column(String, nullable=False)
    reason = Column(String, nullable=False)
    percentage = Column(Float, nullable=False)

class Message(Base):
    __tablename__ = "Messages"
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    hod_name = Column(String, ForeignKey('Department Heads.username'), nullable=False)
    hod_department = Column(String, ForeignKey('Departments.Alias'), nullable=False)
    date = Column(String, nullable=False)
    to = Column(String, nullable=False)
    title = Column(String, nullable=False)
    message = Column(String, nullable=False)
    important = Column(Boolean, nullable=False)


class PendingVerificationImage(Base):
    __tablename__ = "PendingVerification"
    id = Column(String, primary_key=True, unique=True)
    user_username = Column(String, nullable=False)
    user_email = Column(String, nullable=False)
    hod_or_teacher = Column(String, nullable=False)