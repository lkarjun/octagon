from database import Base
from sqlalchemy import Column, Integer, String

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