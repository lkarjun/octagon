from fastapi import APIRouter, Depends, status
from sqlalchemy.orm.session import Session
from sqlalchemy import and_
from typing import List
import Schemas, database, oauth2
from repository import admin


router = APIRouter(tags=['Admin'], prefix='/admin')
get_db = database.get_db
template = admin.AdminTemplates

@router.post('/create_hod', status_code=status.HTTP_201_CREATED, response_model=Schemas.ShowHods)
async def create_hod(request: Schemas.CreateHod, db: Session = Depends(get_db),\
                        admin_or_not: Schemas.Admin = Depends(oauth2.get_admin)):
    return admin.create(request, db)

@router.delete('/delete_hod/{name}/{department}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_hod(name:str, department: str, db: Session = Depends(get_db), \
                    admin_or_not: Schemas.Admin = Depends(oauth2.get_admin)):
    return admin.delete(name, department, db)

@router.put('/edit_hod/{user_name}', status_code=status.HTTP_202_ACCEPTED)
async def update_detail(user_name: str, request: Schemas.CreateHod, db: Session = Depends(get_db),\
                        admin_or_not: Schemas.Admin = Depends(oauth2.get_admin)):
    return admin.update(user_name, request, db)

@router.get('/hods', status_code=status.HTTP_202_ACCEPTED, response_model=List[Schemas.ShowHods])
async def hods_full_details(db: Session = Depends(get_db), admin_or_not: Schemas.Admin = Depends(oauth2.get_admin)):
    return admin.get_all(db)

@router.get('/hods/{user_name}', status_code=status.HTTP_202_ACCEPTED, response_model=Schemas.ShowHods)
async def hod_detail(db: Session = Depends(get_db), user_name = None, admin_or_not: Schemas.Admin = Depends(oauth2.get_admin)):
    return admin.get_one(db, user_name)

@router.put('/update_password', status_code=status.HTTP_202_ACCEPTED)
async def update_admin_password(request: Schemas.AdminPass, db: Session = Depends(get_db), \
                                admin_or_not: Schemas.Admin = Depends(oauth2.get_admin)):
    return admin.change_admin_pass(request, db)