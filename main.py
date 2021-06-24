from fastapi import FastAPI, Request, UploadFile, Form, File, status, Response

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from faceid import decoded_image, Dict, List
from database import engine
import Schemas, models, hashing
from routers import admin

#docs_url=None, redoc_url=None
app = FastAPI()

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
     

@app.post('/login', tags=["Authentication"], status_code=status.HTTP_202_ACCEPTED)
async def login(file: Dict, response: Response):
    decoded_image(file['file'])
    response.status_code = status.HTTP_400_BAD_REQUEST
    return False

@app.post('/Admin_login', tags = ['Admin'])
async def admin_login(request: Schemas.Admin):
    return request

