from fastapi import FastAPI, Request, UploadFile, Form, File
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from faceid import decoded_image, Dict

#docs_url=None, redoc_url=None
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates('templates')


@app.get('/')
async def Login(requset: Request):
    return templates.TemplateResponse('login.html', context={'request': requset})

@app.get('/workspace')
async def workspace(request: Request):
    return templates.TemplateResponse('welcome.html', context={"request": request, "id": 3000})
     

@app.post('/analyse')
async def analyser(file: Dict):
    decoded_image(file['file'])
    return False
    