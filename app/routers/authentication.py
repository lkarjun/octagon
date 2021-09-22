from fastapi import APIRouter, status, Depends, Request, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette.responses import RedirectResponse
from security.faceid import Dict, recogize_user
from security import oauth2, hashing
import templates as temp
from datetime import timedelta
import time

router = APIRouter(tags = ['Authentication'])

@router.post('/octagon/login', status_code=status.HTTP_202_ACCEPTED, response_class=temp.RedirectResponse)
async def login(request: Request, data: OAuth2PasswordRequestForm = Depends()):
    try:
        recogize_result = recogize_user(data)
    except:
        return temp.OthersTemplates.login_page(request, 'block', 'Cant visible your face!😔 Please try again.')

    if not recogize_result:
        return temp.OthersTemplates.login_page(request, 'block', 'Invalid credential!🤔 Please Try again.')

    who, username = data.username.split(";")
    
    if who == 'teacher':
        access_token = oauth2.manager_teacher.create_access_token(
                    data = dict(sub = data.username),
                    expires=timedelta(hours=6)
            )
        res = temp.OthersTemplates.login_redirect_page(request, who)
        oauth2.manager_teacher.set_cookie(res, access_token)
        return res
        
    access_token = oauth2.manager_hod.create_access_token(
                    data = dict(sub = data.username),
                    expires=timedelta(hours=6)
            )
    res = temp.OthersTemplates.login_redirect_page(request, who)
    oauth2.manager_hod.set_cookie(res, access_token)
    return res

@router.get("/octagon/logout/{who}", status_code=status.HTTP_202_ACCEPTED, response_class=temp.RedirectResponse)
async def logout(request: Request, who):
    tokens = {'teacher': 'teacherToken', 'hod': 'hodToken'}
    res = RedirectResponse("/")
    res.delete_cookie(tokens[who])
    return res

@router.post('/admin/login', status_code=status.HTTP_202_ACCEPTED, response_class=temp.RedirectResponse)
async def admin_login(request: Request, data: OAuth2PasswordRequestForm = Depends()):
    username = data.username
    user = await oauth2.get_user(username, return_data = True)
    if not user: return temp.AdminTemplates.admin_login_page(request, 'block')
    if not hashing.Hash.verify(user.password, data.password):
        return temp.AdminTemplates.admin_login_page(request, 'block')

    access_token = oauth2.manager_admin.create_access_token(
                        data = dict(sub = user.name),
                        expires=timedelta(minutes=20)
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