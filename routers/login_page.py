from fastapi import APIRouter
from get_template import OthersTemplates
from fastapi import Request

router = APIRouter(tags = ['LoginPage'])

@router.get('/')
async def home(request: Request):
    return OthersTemplates.login_page(request)