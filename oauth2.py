from fastapi_login import LoginManager
from fastapi_login.exceptions import InvalidCredentialsException
from fastapi.responses import RedirectResponse
import database

class NotAuthenticatedException(Exception):
    pass

def exc_handler(request, exc):
    return RedirectResponse(url='/error')

manager_admin = LoginManager(
                '1fb047dad3e488183c22e1ec5f982cba2daed79f15f0b357',
                token_url='/admin/login',
                use_cookie=True,
                use_header=True,
            )
manager_admin.cookie_name = 'adminToken'

manager_admin.not_authenticated_exception = NotAuthenticatedException

@manager_admin.user_loader
async def get_user(username: str):
    db = database.SessionLocal()
    a = None if username == 'ada' else username
    db.close()
    return a