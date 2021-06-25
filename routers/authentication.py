from fastapi import APIRouter, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from repository import admin
from faceid import decoded_image, Dict

router = APIRouter(tags = ['Authentication'])


@router.post('/admin/login', status_code=status.HTTP_202_ACCEPTED)
async def admin_login(request: OAuth2PasswordRequestForm = Depends()):
    return admin.check_credential(request)

@router.post('/login', tags=["Authentication"], status_code=status.HTTP_202_ACCEPTED)
async def login(file: Dict):
    decoded_image(file['file'])
    return False
