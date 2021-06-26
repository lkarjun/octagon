from fastapi.templating import Jinja2Templates
from fastapi import status

templates = Jinja2Templates('templates')



class AdminTemplates():

    def admin_login_page_(request):
        return templates.TemplateResponse('admin_login.html', 
                context={'request': request, 'title': 'Admin Portal', 'verify': 'none'})

    def login_error(request):
        return templates.TemplateResponse('admin_login.html', 
                context={'request': request, 'title': 'Admin Portal', 'verify': 'block'}, status_code=status.HTTP_401_UNAUTHORIZED)
    
    def login_success(request, header):
        return templates.TemplateResponse('welcome.html', context={'request': request}, headers=header)


class OthersTemplates():
    
    def login_page(request):
        return templates.TemplateResponse('login.html', context={'request': request})