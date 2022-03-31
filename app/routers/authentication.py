from fastapi import APIRouter, status, Depends, Request, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette.responses import RedirectResponse
from security.faceid import Dict, recogize_user
from security import oauth2, hashing
import templates as temp
from sqlalchemy.orm.session import Session
from database import database
from database import models
from sqlalchemy import or_
from datetime import timedelta
import time

router = APIRouter(tags = ['Authentication'])
get_db = database.get_db

@router.post('/octagon/login', status_code=status.HTTP_202_ACCEPTED, response_class=temp.RedirectResponse)
async def login(request: Request, data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    hod = db.query(models.Hod).filter(
                        models.Hod.username == data.username
                    ).first()

    teacher = db.query(models.Teachers).filter(
                        models.Teachers.username == data.username
                    ).first()
                    
    if not (hod or teacher):
        return temp.OthersTemplates.login_page(request, 'block', 'Invalid credential!🤔 Please Try again.')

    if hod and hod.status != "Continue":
        return temp.OthersTemplates.login_page(request, 'block', "Please contact admin! Status is discontinue👋")
    if teacher and teacher.status != "Continue":
        return temp.OthersTemplates.login_page(request, 'block', "Please contact admin! Status is discontinue👋")

    try:
        recogize_result = recogize_user(data)
    except:
        return temp.OthersTemplates.login_page(request, 'block', 'Cant visible your face!😔 Please try again.')

    if not recogize_result:
        print(f"{data.username} failed to login...")
        return temp.OthersTemplates.login_page(request, 'block', 'Invalid credential!🤔 Please Try again.')

    who = 'hod' if hod else 'teacher'
    
    if who == 'teacher':
        access_token = oauth2.manager_teacher.create_access_token(
                    data = dict(sub = f"teacher;{data.username}"),
                    expires=timedelta(hours=6)
            )
        res = temp.OthersTemplates.login_redirect_page(request, who)
        oauth2.manager_teacher.set_cookie(res, access_token)
        print(f"Teacher: {data.username} is successfully loged in...")
        return res
        
    access_token = oauth2.manager_hod.create_access_token(
                    data = dict(sub = f"hod;{data.username}"),
                    expires=timedelta(hours=6)
            )
    res = temp.OthersTemplates.login_redirect_page(request, who)
    oauth2.manager_hod.set_cookie(res, access_token)
    print(f"Hod: {data.username} is successfully loged in...")
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
                        expires=timedelta(hours=6)
                    )
    res = temp.AdminTemplates.login_success_redirect()
    tkn = {'access_token': access_token, 'token_type': 'bearer'}
    oauth2.manager_admin.set_cookie(res, access_token)
    return res

@router.get("/admin/logout", response_class=temp.RedirectResponse)
async def admin_logout(request: Request):
    res = RedirectResponse("/admin/login")
    res.delete_cookie("adminToken")
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