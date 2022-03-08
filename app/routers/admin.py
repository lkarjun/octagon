from fastapi import APIRouter, Depends, status, UploadFile, File, Form, Response, Request, HTTPException
from starlette.background import BackgroundTasks
from templates import AdminTemplates
from sqlalchemy.orm.session import Session
from typing import Dict, List
from database import database
from security import oauth2
from repository import admin, Schemas, verify


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

@router.get("/unverifiedusers")
async def unverified(request: Request, user=Depends(oauth2.manager_admin)):
    return AdminTemplates.unverified(request)

@router.get('/teachers')
async def teachers_list(request: Request, 
                        db: Session = Depends(get_db),
                        user=Depends(oauth2.manager_admin)):
    return AdminTemplates.teachers_list(request, db)


@router.delete('/portal/remove_teacher')

@router.delete('/portal/remove_pending', status_code=status.HTTP_204_NO_CONTENT)
async def remove_pending(request: Schemas.PendingVerification,
                         db: Session = Depends(get_db),
                         user=Depends(oauth2.manager_admin)):
    return verify.remove_pending(request, db)

@router.post("/portal/alert_user", status_code=status.HTTP_204_NO_CONTENT)
async def alert_user(request: Schemas.PendingVerification,
                     bg_task: BackgroundTasks,
                     db: Session = Depends(get_db),
                     user=Depends(oauth2.manager_admin)):
    return verify.alert_user(request, db, bg_task)

@router.post('/portal/create_hod', status_code=status.HTTP_204_NO_CONTENT)
async def create_hod(request: Schemas.CreateHod,
                     bg_task: BackgroundTasks,
                     db: Session = Depends(get_db),
                     user=Depends(oauth2.manager_admin)):
    return admin.create(request, db, bg_task)

# ======================================V2.0=========================================================
# Changes needed here

@router.post('/portal/appoint_hod', status_code=status.HTTP_204_NO_CONTENT)
async def appoint_hod(data: Schemas.Staff_v2_0, 
                      bg_task: BackgroundTasks,
                      db: Session = Depends(get_db),
                      user = Depends(oauth2.manager_admin)):
    return admin.appoint_hod(data, db, bg_task)

@router.post("/portal/add-hod-from-file", status_code=status.HTTP_204_NO_CONTENT)
async def add_hod_from_file(
                            department: str = Form(...),
                            DATA: UploadFile = File(...),
                            ):
    if DATA.content_type not in ['text/csv', 'text/xlxm', 'text/xls']:
        raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# =================================================================================================

@router.delete('/portal/delete_hod', status_code=status.HTTP_204_NO_CONTENT)
async def delete_hod(request: Schemas.DeleteHod, db: Session = Depends(get_db),\
            user=Depends(oauth2.manager_admin)):
    return admin.delete(request, db)

@router.put('/portal/edit_hod/{username}', status_code=status.HTTP_202_ACCEPTED)
async def update_detail(username: str, request: Schemas.CreateHod, db: Session = Depends(get_db),\
            user=Depends(oauth2.manager_admin)):
    return admin.update(username, request, db)

@router.get('/portal/hods', status_code=status.HTTP_202_ACCEPTED, response_model=List[Schemas.ShowHods])
async def hods_full_details(db: Session = Depends(get_db), \
            user=Depends(oauth2.manager_admin)):
    return admin.get_all(db)

@router.get('/portal/hods/{username}', status_code=status.HTTP_202_ACCEPTED, response_model=Schemas.ShowHods)
async def hod_detail(db: Session = Depends(get_db), username = None, user=Depends(oauth2.manager_admin)):
    return admin.get_one(db, username)

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