import pandas as pd
from pathlib import Path
from repository import Schemas
import datetime
from typing import Callable
import functools

# Decorators
BASE_PATH = Path("app/repository/AttendenceFiles")

def get_attendence_files(func: Callable):
    
    @functools.wraps(func)    
    
    def wrap(*args, **kwargs):
        
        open_file = kwargs['open_file'] if 'open_file' in kwargs else True
    
        course, year = kwargs['request'].course, kwargs['request'].year
        daily_path = BASE_PATH/f"{course}{year}.csv"
        monthly_path = BASE_PATH/f"{course}{year}_monthly.csv"
        
        if open_file:
            daily = pd.read_csv(daily_path)
            monthly = pd.read_csv(monthly_path)

            files = Schemas.Files(daily=daily, monthly_path=monthly_path,
                          daily_path=daily_path, monthly=monthly)
            
            return func(*args, **kwargs, files=files)
            
        files = Schemas.Files(daily_path=daily_path, monthly_path=monthly_path)
        
        return func(*args, **kwargs, files=files)
    
    return wrap
    
def save_files(func: Callable):
    @functools.wraps(func)
    
    def wraps(save_monthly = False, *args, **kwargs):
        
        files = func(*args, **kwargs)
        files.daily.to_csv(files.daily_path, index=False)
        
        if save_monthly:
            files.monthly.to_csv(files.monthly_path, index=False)
    
    return wraps
        
def CreateAttendence(total_year: int, course_alias: str):
    path = Path("repository/AttendenceFiles")
    path.mkdir(exist_ok=True)
    
    for i in range(1, total_year + 1):
        attendence = pd.DataFrame(columns = ['StudentsName'])
        monthly_report = pd.DataFrame(columns=['StudentsName'])
        attendence.to_csv(f"repository/AttendenceFiles/{course_alias}{i}.csv", index=False)
        monthly_report.to_csv(f"repository/AttendenceFiles/{course_alias}{i}_monthly.csv", index=False)

@save_files
@get_attendence_files
def admit_students(request: Schemas.AddStudent, files: Schemas.Files):
    full_names = files.daily['StudentsName'].to_list()+[request.name]
    files.daily = pd.DataFrame(data = full_names, columns=files.daily.columns)
    files.monthly = pd.DataFrame(data = full_names, columns=files.daily.columns)
    return files
