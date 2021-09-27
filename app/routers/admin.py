from fastapi import APIRouter, Depends, status, UploadFile, File, Form, Response, Request
from templates import AdminTemplates
from sqlalchemy.orm.session import Session
from typing import Dict, List
from database import database
from security import oauth2
from repository import admin, Schemas


router = APIRouter(tags=['Admin'], prefix='/admin')
get_db = database.get_db

# pages

@router.get("")
async def home():
    return AdminTemplates.login_success_redirect()

@router.get("/details")
async def details(request: Request, db: Session = Depends(get_db),
                    user=Depends(oauth2.manager_admin)):
    return AdminTemplates.details(request, db)

@router.get("/department")
async def department(request: Request, db: Session = Depends(get_db),
                    user=Depends(oauth2.manager_admin)):
    return AdminTemplates.department(request, db)

@router.get("/hod")
async def hod(request: Request, db: Session = Depends(get_db),
                    user=Depends(oauth2.manager_admin)):
    return AdminTemplates.hod(request, db)

@router.get("/credential")
async def credential(request: Request, user=Depends(oauth2.manager_admin)):
    return AdminTemplates.credential(request)

@router.post('/portal/create_hod', status_code=status.HTTP_201_CREATED)
async def create_hod(request: Schemas.CreateHod, db: Session = Depends(get_db), user=Depends(oauth2.manager_admin)):
    return admin.create(request, db)

@router.post('/portal/verification_image', status_code=status.HTTP_204_NO_CONTENT)
async def verification_image(username: str = Form(...),
                            image1: UploadFile = File(...),
                            image2: UploadFile = File(...),
                            image3: UploadFile = File(...),   
                            user = Depends(oauth2.manager_admin)):
    image1, image2, image3 = await image1.read(), await image2.read(),\
                                await image3.read()
    return admin.verification_image(username, image1, image2, image3)

@router.delete('/portal/delete_hod', status_code=status.HTTP_204_NO_CONTENT)
async def delete_hod(request: Schemas.DeleteHod, db: Session = Depends(get_db),\
            user=Depends(oauth2.manager_admin)):
    return admin.delete(request, db)

@router.put('/portal/edit_hod/{user_name}', status_code=status.HTTP_202_ACCEPTED)
async def update_detail(user_name: str, request: Schemas.CreateHod, db: Session = Depends(get_db),\
            user=Depends(oauth2.manager_admin)):
    return admin.update(user_name, request, db)

@router.get('/portal/hods', status_code=status.HTTP_202_ACCEPTED, response_model=List[Schemas.ShowHods])
async def hods_full_details(db: Session = Depends(get_db), \
            user=Depends(oauth2.manager_admin)):
    return admin.get_all(db)

@router.get('/portal/hods/{user_name}', status_code=status.HTTP_202_ACCEPTED, response_model=Schemas.ShowHods)
async def hod_detail(db: Session = Depends(get_db), user_name = None, user=Depends(oauth2.manager_admin)):
    return admin.get_one(db, user_name)

@router.put('/portal/update_password', status_code=status.HTTP_202_ACCEPTED)
async def update_admin_password(request: Schemas.AdminPass, db: Session = Depends(get_db),\
            user=Depends(oauth2.manager_admin)):
    return admin.change_admin_pass(request, db)

@router.post('/portal/Adddepartment', status_code=status.HTTP_201_CREATED)
async def add_department(request: Schemas.AddDepartment, db: Session = Depends(get_db),\
                user=Depends(oauth2.manager_admin)):
    return admin.new_department(request, db)

@router.get('/portal/departments', status_code=status.HTTP_202_ACCEPTED, response_model=List)
async def all_departments(db: Session = Depends(get_db), user=Depends(oauth2.manager_admin)):
    return admin.get_all_departments(db)

@router.delete('/portal/deletedepartment', status_code=status.HTTP_204_NO_CONTENT)
async def delete_department(request: Schemas.DeleteDepartment, db: Session = Depends(get_db),\
                    user=Depends(oauth2.manager_admin)):
    return admin.delete_department(request, db)

@router.post('/portal/AddCourse', status_code=status.HTTP_201_CREATED)
async def add_course(request: Schemas.AddCourse, db: Session = Depends(get_db),\
            user=Depends(oauth2.manager_admin)):
    return admin.add_course(request, db)

@router.delete('/portal/deletecourse', status_code=status.HTTP_201_CREATED)
async def delete_course(request: Schemas.DeleteCourse, db: Session = Depends(get_db), \
            user=Depends(oauth2.manager_admin)):
    return admin.delete_course(request, db)

@router.get('/portal/courses', status_code=status.HTTP_202_ACCEPTED, response_model=List)
async def get_all_courses(db: Session = Depends(get_db), user=Depends(oauth2.manager_admin)):
    return admin.get_all_course(db)

@router.post('/portal/reset_password', status_code=status.HTTP_202_ACCEPTED)
async def reset(request: Schemas.AdminPass, db: Session = Depends(get_db), user=Depends(oauth2.manager_admin)):
    return admin.reset_pass(request, db)