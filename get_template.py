from fastapi.templating import Jinja2Templates
from fastapi import status
from starlette.responses import RedirectResponse

templates = Jinja2Templates('templates')



class AdminTemplates():

    def admin_login_page(request):
        return templates.TemplateResponse('admin_login.html', 
                context={'request': request, 'title': 'Admin Portal', 'verify': 'none'})

    def login_success(request):
        return templates.TemplateResponse('welcome.html', context={'request': request})

    def login_success_redirect():
        return RedirectResponse(url = '/admin/portal', status_code=status.HTTP_302_FOUND)

class OthersTemplates():
    
    def login_page(request):
        return templates.TemplateResponse('login.html', context={'request': request})