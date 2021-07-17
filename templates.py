from fastapi.templating import Jinja2Templates
from fastapi import status
from fastapi.responses import RedirectResponse
from repository import admin
from database import database
from collections import defaultdict

templates = Jinja2Templates('templates')



class AdminTemplates():

    def admin_login_page(request, verify = 'none'):
        return templates.TemplateResponse('admin_login.html', 
                context={'request': request, 'title': 'Admin Login', 'verify': verify})

    def login_success(request):
        courses_with_department = defaultdict(lambda: [])
        db = database.SessionLocal()
        hods = admin.get_all(db)
        dep = admin.get_all_departments(db)
        course = admin.get_all_course(db)

        for i in course: courses_with_department[i.Department].append(i.Course_name_alias)
        db.close()
        return templates.TemplateResponse('adminPortal.html', 
                    context={'request': request, 'title': 'Admin Portal', 'hods': hods, 'dep': dep, 'course': course, 'cw': courses_with_department})

    def login_success_redirect():
        return RedirectResponse(url = '/admin', status_code=status.HTTP_302_FOUND)


    def login_error_redirect():
        return RedirectResponse(url='/admin/login', status_code=status.HTTP_302_FOUND)


class OthersTemplates():
    
    def login_page(request):
        return templates.TemplateResponse('login.html', context={'request': request})