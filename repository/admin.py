from sqlalchemy.orm.session import Session
import Schemas, models, hashing
from fastapi import status, HTTPException, Response
from sqlalchemy import and_


def change_admin_pass(request: Schemas.AdminPass, db: Session):
    admin_pass = db.query(models.Admin).filter(models.Admin.name == request.username)
    
    if not admin_pass.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid Credentials")
    
    if not hashing.Hash.verify(admin_pass.first().password, request.current_pass):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Incorrect password")
    # generate a jwt token and return it
    updating = {'name': request.username, 'password': hashing.Hash.bcrypt(request.new_pass)}
    admin_pass.update(updating)
    db.commit()
    return 'changed'

def get_all(db: Session):
    hods = db.query(models.Hod).all()
    if not hods:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,\
            detail = 'No content in the database')
    return hods

def get_one(db: Session, user_name: str):
    if user_name is None: return 'Please pass hod name to get details'
    hod = db.query(models.Hod).filter(models.Hod.user_name == user_name).first()
    if not hod:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,\
            detail = f'THERE IS NO HOD IN USER NAME: {user_name}')
    return hod  

def update(user_name: str, request: Schemas.CreateHod, db: Session):
    hod = db.query(models.Hod).filter(models.Hod.user_name == user_name)
    if not hod.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Alert No User with {user_name}") 
    hod.update(dict(request))
    db.commit()
    return 'done'

def delete(name:str, department: str, db: Session):
    hod = db.query(models.Hod).filter(and_(models.Hod.name == name,
                                models.Hod.department == department))
    if not hod.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Alert No User with name: {name} and department: {department}") 

    hod.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=204)

def create(request: Schemas.CreateHod, db: Session):
    new_hod = models.Hod(name = request.name, email = request.email, \
                        phone_num = request.phone_num, user_name = request.user_name, \
                        department = request.department)
    db.add(new_hod)
    db.commit()
    db.refresh(new_hod)
    return new_hod

def new_department(request: Schemas.AddDepartment, db: Session):
    department = models.Departments(Department = request.Department, Alias = request.Alias)
    db.add(department)
    db.commit()
    db.refresh(department)
    return "Department Added"

def get_all_departments(db: Session):
    departments = db.query(models.Departments).all()
    if not departments:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,\
            detail = 'No content in the database')
    return departments

def delete_department(request: Schemas.AddDepartment, db: Session):
    depart = db.query(models.Departments).filter(and_(models.Departments.Alias == request.Alias,
                                            models.Departments.Department == request.Department))
    if not depart.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,\
                    detail=f"No Department in name {request.Department} and alias {request.Alias}") 
    depart.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=204)