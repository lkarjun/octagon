from fastapi.templating import Jinja2Templates
from fastapi import status
from fastapi.responses import RedirectResponse
from repository import admin, hod
from database import database
from collections import defaultdict

templates = Jinja2Templates('templates')



class AdminTemplates():

    def admin_login_page(request, verify = 'none'):
        return templates.TemplateResponse('admin_login.html', 
                context={'request': request, 'title': 'ADMIN LOGIN', 'verify': verify})

    def login_success(request):
        courses_with_department = defaultdict(lambda: [])
        db = database.SessionLocal()
        hods = admin.get_all(db)
        dep = admin.get_all_departments(db)
        course = admin.get_all_course(db)

        for i in course: courses_with_department[i.Department].append(i.Course_name_alias)
        db.close()
        return templates.TemplateResponse('adminPortal.html', 
                    context={'request': request, 'title': 'ADMIN PORTAL',
                            'hods': hods, 'dep': dep, 'course': course, 
                            'cw': courses_with_department})

    def login_success_redirect():
        return RedirectResponse(url = '/admin', status_code=status.HTTP_302_FOUND)


    def login_error_redirect():
        return RedirectResponse(url='/admin/login', status_code=status.HTTP_302_FOUND)


class OthersTemplates():
    
    def login_page(request):
        return templates.TemplateResponse('login.html', context={'request': request})


class HodTemplates():

    def timetable(request):
        db = database.SessionLocal()
        courses = admin.get_all_course(db)
        teachers = hod.get_techer_details(db)
        depart = admin.get_all_departments(db)
        db.close()
        return templates.TemplateResponse('timeTable.html', 
                context={'request': request, 'title': 'TIME TABLE', 
                        'courses': courses, 'teachers': teachers, 'department': depart})

    def appoint_teacher(request):
        return templates.TemplateResponse("appointTeacher.html",
                context={'request': request, "title": "APPOINT TEACHERS"})

    def uoc_notification(request):
        notifications = hod.uoc.get_notifications()
        return templates.TemplateResponse("uocNotification.html",
                context={"request": request, "title": "UOC NOTIFICATION", "notfy": notifications})
    
    def attendenceDataView(request):
        return templates.TemplateResponse("attendenceDataView.html",
                context={"request": request, "title": "Attendence Data"})

    def takeAttendence(request):
        tmp = templates.TemplateResponse("takeAttendence.html",
                context={"request": request, "title": "Students Attendence",
                         "who":"hod"})

        return tmp

class TeacherTemplates():
    
    def takeAttendence(request):
        tmp = templates.TemplateResponse("takeAttendence.html",
                context={"request": request, "title": "Students Attendence",
                    "who":"teacher"})

        return tmp

    def addStudents(request):
        tmp = templates.TemplateResponse("addStudent.html",
                context={"request": request, "title": "Add Students"})
        return tmp