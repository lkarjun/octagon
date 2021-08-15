from fastapi.templating import Jinja2Templates
from fastapi import status
from fastapi.responses import RedirectResponse
from repository import admin, hod, attendence
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
        hods = admin.get_all(db, template=True)
        dep = admin.get_all_departments(db, template=True)
        course = admin.get_all_course(db, template=True)

        for i in course: courses_with_department[i.Department].append(i.Course_name_alias)
        db.close()
        return templates.TemplateResponse('adminPortal.html', 
                    context={'request': request, 'title': 'Admin Portal',
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
                context={'request': request, 'title': 'Time Table', 
                        'courses': courses, 'teachers': teachers, 'department': depart})

    def appoint_teacher(request):
        db = database.SessionLocal()
        teachers = hod.get_techer_details(db, template=True)
        depart = admin.get_all_departments(db, template=True)
        db.close()
        tmp = templates.TemplateResponse("appointTeacher.html",
                context={'request': request, "title": "Appoint Teachers", 
                         "teachers": teachers, "depart": depart})
        return tmp

    def uoc_notification(request):
        notifications = hod.uoc.get_notifications()
        return templates.TemplateResponse("uocNotification.html",
                context={"request": request, "title": "UOC Notification", "notfy": notifications})
    
    def attendenceDataView(request):
        db = database.SessionLocal()
        courses = admin.get_all_course(db)
        db.close()
        tmp = templates.TemplateResponse("attendenceDataView.html",
                context={"request": request, "title": "Attendence Data",
                        "course": courses})
        return tmp

    def takeAttendence(request):
        db = database.SessionLocal()
        courses = admin.get_all_course(db)
        db.close()
        tmp = templates.TemplateResponse("takeAttendence.html",
                context={"request": request, "title": "Students Attendence",
                         "who":"hod", "course": courses})

        return tmp

    def show_attendence_data(request, data):
        column, values = attendence.show_attendence_data(request=data)
        tmp = templates.TemplateResponse("showAttendenceData.html",
                    context={"request": request, "title": "Attendence Sheet",
                                "column": column, "values": values, "data": data})

        return tmp

    def show_student_details(request, course, year):
        db = database.SessionLocal()
        details = hod.get_student_details(db, course, year)
        db.close()
        tmp = templates.TemplateResponse("studentDetails.html",
                    context={"request": request, "title": "Attendence Sheet",
                                "details": details, "course": course, "year": year})

        return tmp

    def show_most_absentees(request, data):
        most_absentee, there_is, working_days = attendence.most_absentee(request=data, open_daily=True)
        tmp = templates.get_template("__mostabsentee.html")
        tmp = tmp.render(request = request, mostabsentee = most_absentee, 
                         there_is=there_is, working_days = working_days)
        return tmp


    def show_report(request, data):
        final_report = attendence.attendence_analysing(request=data, open_daily=True).values
        tmp = templates.get_template("__attendencereport.html")
        tmp = tmp.render(request = request, final_report = final_report)
        return tmp



class TeacherTemplates():
    
    def takeAttendence(request):
        db = database.SessionLocal()
        courses = admin.get_all_course(db)
        db.close()
        tmp = templates.TemplateResponse("takeAttendence.html",
                context={"request": request, "title": "Students Attendence",
                         "who":"teacher", "course": courses})

        return tmp

    def addStudents(request):
        db = database.SessionLocal()
        courses = admin.get_all_course(db)
        db.close()

        tmp = templates.TemplateResponse("addStudent.html",
                context={"request": request, "title": "Add Students",
                         "course": courses})
        return tmp