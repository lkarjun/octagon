from fastapi import APIRouter, status, Depends, Response, Request
from fastapi.security import OAuth2PasswordRequestForm
from repository import admin
from faceid import decoded_image, Dict
from sqlalchemy.orm import Session
import database

router = APIRouter(tags = ['Authentication'])


@router.post('/admin/workspace', status_code=status.HTTP_202_ACCEPTED, tags=['AdminPages'])
async def admin_login(req:Request, response: Response, request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    return admin.check_credential(req, request, db, response)

@router.post('/login', status_code=status.HTTP_202_ACCEPTED)
async def login(file: Dict):
    decoded_image(file['file'])
    return False
