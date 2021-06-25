from fastapi import FastAPI, Request, UploadFile, Form, File, status
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from database import engine
import models
from routers import admin, authentication

#docs_url=None, redoc_url=None
app = FastAPI()

app.include_router(authentication.router)
app.include_router(admin.router)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates('templates')

models.Base.metadata.create_all(engine)


@app.get('/')
async def home(requset: Request):
    return templates.TemplateResponse('login.html', context={'request': requset})

@app.get('/workspace', tags=['Workspace'])
async def workspace(request: Request):
    return templates.TemplateResponse('welcome.html', context={"request": request, "id": 3000})


