from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from database import engine
import models
from routers import admin, authentication, login_page, admin_pages
from get_template import templates

#docs_url=None, redoc_url=None
app = FastAPI(debug=True)

app.include_router(authentication.router)
app.include_router(admin.router)
app.include_router(admin_pages.router)
app.include_router(login_page.router)

app.mount("/static", StaticFiles(directory="static"), name="static")


models.Base.metadata.create_all(engine)



@app.get('/workspace', tags=['HOD'])
async def workspace(request: Request):
    return templates.TemplateResponse('welcome.html', context={"request": request, "id": 3000})


