from fastapi import APIRouter, status, Depends, Request, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from security.faceid import decoded_image, Dict
from security import oauth2, hashing
import templates as temp


router = APIRouter(tags = ['Authentication'])

@router.post('/login', status_code=status.HTTP_202_ACCEPTED)
async def login(file: Dict):
    decoded_image(file['file'])
    return False

@router.post('/admin/login', status_code=status.HTTP_202_ACCEPTED, response_class=temp.RedirectResponse)
async def admin_login(request: Request, data: OAuth2PasswordRequestForm = Depends()):
    username = data.username
    user = await oauth2.get_user(username, return_data = True)
    if not user: return temp.AdminTemplates.admin_login_page(request, 'block')
    if not hashing.Hash.verify(user.password, data.password):
        return temp.AdminTemplates.admin_login_page(request, 'block')

    access_token = oauth2.manager_admin.create_access_token(
                        data = dict(sub = user.name)
                    )
    res = temp.AdminTemplates.login_success_redirect()
    tkn = {'access_token': access_token, 'token_type': 'bearer'}
    oauth2.manager_admin.set_cookie(res, access_token)
    return res

@router.post('/error', status_code=status.HTTP_401_UNAUTHORIZED)
async def error():
    return temp.AdminTemplates.admin_login_page(Request, 'block')

@router.get('/error', status_code=status.HTTP_401_UNAUTHORIZED)
async def error():
    return temp.AdminTemplates.login_error_redirect()

@router.put('/error', status_code=status.HTTP_401_UNAUTHORIZED)
async def error():
    return {'Error': "Warning"}

@router.delete('/error', status_code=status.HTTP_401_UNAUTHORIZED)
async def error():
    return {'Error': "Warning"}