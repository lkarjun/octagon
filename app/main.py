from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from database import models, database
from security import oauth2
from routers import admin, authentication, pages, hod, teacher, attendence

tags_metadata = [
    {
        "name": "Head Of Department",
        "description": "Hod's unique functionalities. Only Hod can appoint new teachers, Admin can't...",
    },
    {
        "name": "Admin",
        "description": "The main role of admin is to: appoint new hod, add / delete collage course and departments...",
    },
    {
        "name": "Authentication",
        "description": "Authentication is required for everyone.",
    },
    {
        "name": "Pages",
        "description": "All webpages...",
    },
]

description = """
**This is my final year Project(Bca)**.
Modified the existing 

system so a teacher 
can logon to the app using their **Face**.

**Also we introduced some more unique features that is**:

* hod can now set timetable without any conflits.
* hod can send emails to other hods and teachers directly.
                     
"""

#docs_url=None, redoc_url=None
app = FastAPI(
            debug=True,
            title="Teachers' Login",
            openapi_tags=tags_metadata,
            description=description,
            redoc_url=None
    )

app.include_router(hod.router)
app.include_router(teacher.router)
app.include_router(attendence.router)
app.include_router(authentication.router)
app.include_router(admin.router)
app.include_router(pages.router)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_exception_handler(oauth2.NotAuthenticatedException, oauth2.exc_handler)

app.add_exception_handler(oauth2.NotAuthenticatedStaff, oauth2.exc_handler_teacher)

models.Base.metadata.create_all(database.engine)
