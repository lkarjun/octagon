from fastapi import APIRouter, status, Request, Depends
from templates import OthersTemplates, AdminTemplates
from security import oauth2

router = APIRouter(tags = ['Pages'])

@router.get('/', status_code=status.HTTP_200_OK)
async def home(request: Request):
    return OthersTemplates.login_page(request)

@router.get('/workspace', status_code=status.HTTP_200_OK)
async def workspace(request: Request):
    return AdminTemplates.login_success(request)

@router.get('/admin/login', status_code=status.HTTP_200_OK)
def admin_login_page(request: Request):
    return AdminTemplates.admin_login_page(request)

@router.get("/admin")
def admin_portal(request: Request, user=Depends(oauth2.manager_admin)):
    return AdminTemplates.login_success(request)

@router.get('hod/workspace')
async def workspace(request: Request):
    return {"Okay": "gotit"}
