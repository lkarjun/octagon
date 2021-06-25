from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

templates = Jinja2Templates('templates')



class AdminTemplates():

    def admin_login_page_(request):
        return templates.TemplateResponse('admin_login.html', 
                context={'request': request, 'title': 'Admin Portal', 'verify': 'none'})

    def login_error(request):
        return templates.TemplateResponse('admin_login.html', 
                context={'request': request, 'title': 'Admin Portal', 'verify': 'block'})
    
    def login_success(request):
        return templates.TemplateResponse('welcome.html', context={'request': request})

    def login_sucess_redirect(status):
        return RedirectResponse(url = '/admin/workspace', status_code=status)
