from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from get_template import AdminTemplates

router = APIRouter()

@router.get('/admin', tags=['AdminPages'], response_class=HTMLResponse)
async def admin_login_page(request: Request):
    return AdminTemplates.admin_login_page_(request)
