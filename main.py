from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from database import engine
import models, oauth2
from routers import admin, authentication, pages

#docs_url=None, redoc_url=None
app = FastAPI(debug=True)

app.include_router(authentication.router)
app.include_router(admin.router)
app.include_router(pages.router)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_exception_handler(oauth2.NotAuthenticatedException, oauth2.exc_handler)

models.Base.metadata.create_all(engine)
