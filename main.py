from fastapi import FastAPI, Request, UploadFile, Form, File
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import numpy as np
from io import BytesIO
from PIL import Image
import base64


app = FastAPI(debug=False)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates('templates')


@app.get('/')
async def home(requset: Request):
    return templates.TemplateResponse('login.html', context={'request': requset})

@app.get('/workspace/{id}')
async def workspace(request: Request, id: int):
    return templates.TemplateResponse('welcom.html', context={"request": request, "id": id})
     

@app.get('/analyse')
async def analyser(file: str, username: str):
    print(username)
    img = base64.b64decode(file)
    img = Image.open(BytesIO(img))
    array = np.asarray(img)
    print(array.shape)
    return '/workspace/3'