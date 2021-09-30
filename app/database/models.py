from database.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean
from sqlalchemy.orm import relationship

class Hod(Base):
    __tablename__ = 'Hod'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    phone_num = Column(String)
    user_name = Column(String)
    department = Column(String)

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

class Teachers(Base):
    __tablename__ = 'Teachers'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    username = Column(String, unique=True)
    department = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone_number = Column(String, nullable=True)
    tag = Column(String)

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

class Students(Base):
    __tablename__ = 'Students'
    id = Column(String, primary_key=True)
    name = Column(String)
    email = Column(String)
    parent_name = Column(String)
    parent_number = Column(Integer)
    parent_number_alt = Column(Integer)
    course = Column(String)
    year = Column(Integer)
    department = Column(String)

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