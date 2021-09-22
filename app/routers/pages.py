from fastapi import APIRouter, status, Request, Depends
from templates import OthersTemplates, AdminTemplates, RedirectResponse
from security import oauth2
from fastapi.responses import RedirectResponse

router = APIRouter(tags = ['Pages'])

@router.get('/octagon/login', status_code=status.HTTP_200_OK)
async def home(request: Request):
    return OthersTemplates.login_page(request)


@router.get('/admin/login', status_code=status.HTTP_200_OK)
def admin_login_page(request: Request):
    return AdminTemplates.admin_login_page(request)

@router.get("/admin")
def admin_portal(request: Request, user=Depends(oauth2.manager_admin)):
    return AdminTemplates.login_success(request)

@router.get("/")
async def common_home(request: Request):
    cookies = request.cookies
    
    if ('hodToken' in cookies) or ('teacherToken' in cookies):
        if 'hodToken' in cookies and 'teacherToken' in cookies:
            if (len(cookies['hodToken']) > 10) and (len(cookies['teacherToken']) > 10):
                res = RedirectResponse('/octagon/login')
                res.delete_cookie('hodToken')
                res.delete_cookie('teacherToken')
                return res
            return RedirectResponse('/octagon/login')
        elif 'hodToken' in cookies and len(cookies['hodToken']) > 10:
            return RedirectResponse('/hod/workspace')
        elif 'teacherToken' in cookies and len(cookies['teacherToken']) > 10:
            return RedirectResponse('/teacher/workspace')
        else:
            return RedirectResponse('/octagon/login')
    else:
        return RedirectResponse('/octagon/login')