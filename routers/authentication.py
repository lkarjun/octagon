from fastapi import APIRouter, status, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from security.faceid import decoded_image, Dict
from security import oauth2
import get_template


router = APIRouter(tags = ['Authentication'])

@router.post('/login', status_code=status.HTTP_202_ACCEPTED)
async def login(file: Dict):
    decoded_image(file['file'])
    return False

@router.post('/admin/login', status_code=status.HTTP_202_ACCEPTED, response_class=get_template.RedirectResponse)
async def admin_login(request: Request, data: OAuth2PasswordRequestForm = Depends()):
    username = data.username
    user = await oauth2.get_user(username)
    if not user: raise oauth2.InvalidCredentialsException

    access_token = oauth2.manager_admin.create_access_token(
                        data = dict(sub = user)
                    )
    res = get_template.AdminTemplates.login_success_redirect()
    tkn = {'access_token': access_token, 'token_type': 'bearer'}
    oauth2.manager_admin.set_cookie(res, access_token)
    return res

@router.post('/error', status_code=status.HTTP_401_UNAUTHORIZED)
async def error():
    return get_template.AdminTemplates.login_error_redirect()

@router.get('/error', status_code=status.HTTP_401_UNAUTHORIZED)
async def error():
    return get_template.AdminTemplates.login_error_redirect()

@router.put('/error', status_code=status.HTTP_401_UNAUTHORIZED)
async def error():
    return {'Error': "Warning"}

@router.delete('/error', status_code=status.HTTP_401_UNAUTHORIZED)
async def error():
    return {'Error': "Warning"}