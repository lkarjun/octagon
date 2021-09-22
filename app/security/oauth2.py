from fastapi_login import LoginManager
from fastapi_login.exceptions import InvalidCredentialsException
from fastapi.responses import RedirectResponse
from database import database, models

class NotAuthenticatedException(Exception):
    pass

def exc_handler(request, exc):
    return RedirectResponse(url='/error')

class NotAuthenticatedStaff(Exception):
    pass

def exc_handler_teacher(request, exc):
    return RedirectResponse(url='/octagon/login')


# Admin login manager
manager_admin = LoginManager(
                '1fb047dad3e488183c22e1ec5f982cba2daed79f15f0b357',
                token_url='/admin/login',
                use_cookie=True,
                use_header=True,
            )
manager_admin.cookie_name = 'adminToken'

manager_admin.not_authenticated_exception = NotAuthenticatedException

@manager_admin.user_loader
async def get_user(username: str, return_data = False):
    db = database.SessionLocal()
    data = db.query(models.Admin).first()
    db.close()
    if return_data:
        return data if username == data.name else None
    return True if username == data.name else None


# Teacher Login Manager

manager_teacher = LoginManager(
                '9e3a3f0afd04dbdb78b5ef16f90c0d6bb8eb0a2c9915df0f',
                token_url='/octagon/login',
                use_cookie=True,
                use_header=True,
            )

manager_teacher.cookie_name = 'teacherToken'
manager_teacher.not_authenticated_exception = NotAuthenticatedStaff

@manager_teacher.user_loader
async def get_teacher(username: str):
    who, username = username.split(";")
    db = database.SessionLocal()
    username = db.query(models.Teachers).filter(
            models.Teachers.username == username).first()
    db.close()
    return username


# Hod Login Manager

manager_hod = LoginManager(
                '5511d4a2ef7f9cb9b30de5663affae95f9445d7b2d3125a9',
                token_url='/octagon/login',
                use_cookie=True,
                use_header=True,
            )

manager_hod.cookie_name = 'hodToken'
manager_hod.not_authenticated_exception = NotAuthenticatedStaff

@manager_hod.user_loader
async def get_hod(username: str):
    who, username = username.split(";")
    db = database.SessionLocal()
    username = db.query(models.Hod).filter(
            models.Hod.user_name == username).first()
    db.close()
    return username