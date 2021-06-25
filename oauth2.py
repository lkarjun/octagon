from fastapi import Depends, HTTPException, status 
from fastapi.security import OAuth2PasswordBearer
import login_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/admin/login")
oauth2_scheme_hodlogin = OAuth2PasswordBearer(tokenUrl="/hod/login")

def get_admin(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return login_token.verify_token(token, credentials_exception)

def get_teacher_name(token: str = Depends(oauth2_scheme_hodlogin)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )