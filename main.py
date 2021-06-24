from os import stat
from fastapi import FastAPI, Request, UploadFile, Form, File, status, Response, Depends, HTTPException

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm.session import Session
from sqlalchemy import and_
from sqlalchemy.sql.functions import user
from faceid import decoded_image, Dict
from database import SessionLocal, engine
import Schemas
import models

#docs_url=None, redoc_url=None
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates('templates')

models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get('/')
async def home(requset: Request):
    return templates.TemplateResponse('login.html', context={'request': requset})

@app.get('/workspace', tags=['Workspace'])
async def workspace(request: Request):
    return templates.TemplateResponse('welcome.html', context={"request": request, "id": 3000})
     

@app.post('/login', tags=["Authentication"], status_code=status.HTTP_202_ACCEPTED)
async def login(file: Dict, response: Response):
    decoded_image(file['file'])
    response.status_code = status.HTTP_400_BAD_REQUEST
    return False
    
@app.post('/create_hod', tags=['Admin'], status_code=status.HTTP_201_CREATED, response_model=Schemas.ShowHods)
async def create_hod(request: Schemas.CreateHod, db: Session = Depends(get_db)):
    new_hod = models.Hod(name = request.name, email = request.email, \
                        phone_num = request.phone_num, user_name = request.user_name, \
                        department = request.department)
    db.add(new_hod)
    db.commit()
    db.refresh(new_hod)
    return new_hod

@app.delete('/delete_hod/{name}/{department}', tags=['Admin'], status_code=status.HTTP_204_NO_CONTENT)
async def delete_hod(name:str, department: str, db: Session = Depends(get_db)):
    hod = db.query(models.Hod).filter(and_(models.Hod.name == name,
                                models.Hod.department == department))
    if not hod.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Alert No User with name: {name} and department: {department}") 

    hod.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=204)

@app.put('/edit_hod/{user_name}', tags=['Admin'], status_code=status.HTTP_202_ACCEPTED)
async def edit_hod(user_name: str, request: Schemas.CreateHod, db: Session = Depends(get_db)):
    hod = db.query(models.Hod).filter(models.Hod.user_name == user_name)
    if not hod.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Alert No User with {user_name}") 
    hod.update(dict(request))
    db.commit()
    return "Done"

@app.get('/hods', tags=['Admin'], status_code=status.HTTP_202_ACCEPTED)
async def hods_full_details(db: Session = Depends(get_db)):
    hods = db.query(models.Hod).all()
    if not hods:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,\
            detail = 'No content in the database')
    return hods

@app.get('/hods/{user_name}', tags = ['Admin'], status_code=status.HTTP_202_ACCEPTED, response_model=Schemas.ShowHods)
async def hod_detail(db: Session = Depends(get_db), user_name = None):
    if user_name is None: return 'Please pass hod name to get details'
    hod = db.query(models.Hod).filter(models.Hod.user_name == user_name).first()
    if not hod:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,\
            detail = f'THERE IS NO HOD IN USER NAME: {user_name}')
    return hod

