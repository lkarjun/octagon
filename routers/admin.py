from fastapi import APIRouter, Depends, status, UploadFile, File, Form, Response
from sqlalchemy.orm.session import Session
from typing import Dict, List
from database import database
from security import oauth2
from repository import admin, Schemas


router = APIRouter(tags=['Admin'], prefix='/admin/portal')
get_db = database.get_db

@router.post('/create_hod', status_code=status.HTTP_201_CREATED)
async def create_hod(request: Schemas.CreateHod, db: Session = Depends(get_db), user=Depends(oauth2.manager_admin)):
    return admin.create(request, db)

@router.post('/verification_image', status_code=status.HTTP_204_NO_CONTENT)
async def verification_image(username: str = Form(...),
                            image1: UploadFile = File(...),
                            image2: UploadFile = File(...),
                            image3: UploadFile = File(...),   
                            user = Depends(oauth2.manager_admin)):
    print(image1.filename, username)
    return Response(status_code=204)

@router.delete('/delete_hod', status_code=status.HTTP_204_NO_CONTENT)
async def delete_hod(request: Schemas.DeleteHod, db: Session = Depends(get_db),\
            user=Depends(oauth2.manager_admin)):
    return admin.delete(request, db)

@router.put('/edit_hod/{user_name}', status_code=status.HTTP_202_ACCEPTED)
async def update_detail(user_name: str, request: Schemas.CreateHod, db: Session = Depends(get_db),\
            user=Depends(oauth2.manager_admin)):
    return admin.update(user_name, request, db)

@router.get('/hods', status_code=status.HTTP_202_ACCEPTED, response_model=List[Schemas.ShowHods])
async def hods_full_details(db: Session = Depends(get_db), \
            user=Depends(oauth2.manager_admin)):
    return admin.get_all(db)

@router.get('/hods/{user_name}', status_code=status.HTTP_202_ACCEPTED, response_model=Schemas.ShowHods)
async def hod_detail(db: Session = Depends(get_db), user_name = None, user=Depends(oauth2.manager_admin)):
    return admin.get_one(db, user_name)

@router.put('/update_password', status_code=status.HTTP_202_ACCEPTED)
async def update_admin_password(request: Schemas.AdminPass, db: Session = Depends(get_db),\
            user=Depends(oauth2.manager_admin)):
    return admin.change_admin_pass(request, db)

@router.post('/Adddepartment', status_code=status.HTTP_201_CREATED)
async def add_department(request: Schemas.AddDepartment, db: Session = Depends(get_db),\
                user=Depends(oauth2.manager_admin)):
    return admin.new_department(request, db)

@router.get('/departments', status_code=status.HTTP_202_ACCEPTED, response_model=List)
async def all_departments(db: Session = Depends(get_db), user=Depends(oauth2.manager_admin)):
    return admin.get_all_departments(db)

@router.delete('/deletedepartment', status_code=status.HTTP_204_NO_CONTENT)
async def delete_department(request: Schemas.DeleteDepartment, db: Session = Depends(get_db),\
                    user=Depends(oauth2.manager_admin)):
    return admin.delete_department(request, db)

@router.post('/AddCourse', status_code=status.HTTP_201_CREATED)
async def add_course(request: Schemas.AddCourse, db: Session = Depends(get_db),\
            user=Depends(oauth2.manager_admin)):
    return admin.add_course(request, db)

@router.delete('/deletecourse', status_code=status.HTTP_201_CREATED)
async def delete_course(request: Schemas.DeleteCourse, db: Session = Depends(get_db), \
            user=Depends(oauth2.manager_admin)):
    return admin.delete_course(request, db)

@router.get('/courses', status_code=status.HTTP_202_ACCEPTED, response_model=List)
async def get_all_courses(db: Session = Depends(get_db), user=Depends(oauth2.manager_admin)):
    return admin.get_all_course(db)