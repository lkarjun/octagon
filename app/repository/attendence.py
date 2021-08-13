from fastapi import HTTPException, status, Response
import pandas as pd
from pathlib import Path
from repository import Schemas
import datetime
from typing import Callable
import functools

# Decorators
BASE_PATH = Path("repository/AttendenceFiles")

def get_attendence_files(func: Callable):
    
    @functools.wraps(func)    
    
    def wrap(*args, **kwargs):
        
        open_files = kwargs['open_file'] if 'open_file' in kwargs else True
        open_daily = kwargs['open_daily'] if 'open_daily' in kwargs else False
    
        course, year = kwargs['request'].course, kwargs['request'].year
        daily_path = BASE_PATH/f"{course}{year}.csv"
        monthly_path = BASE_PATH/f"{course}{year}_monthly.csv"
        
        if open_files:
            daily = pd.read_csv(daily_path)
            monthly = pd.read_csv(monthly_path) if open_daily else None

            files = Schemas.Files(daily=daily, monthly_path=monthly_path,
                          daily_path=daily_path, monthly=monthly)
            
            return func(*args, **kwargs, files=files)
            
        files = Schemas.Files(daily_path=daily_path, monthly_path=monthly_path)
        
        return func(*args, **kwargs, files=files)
    
    return wrap
    
def save_files(func: Callable):
    @functools.wraps(func)
    
    def wraps(*args, **kwargs):
                
        save_monthly = kwargs['save_monthly'] if 'save_monthly' in kwargs else False
        only_monthly = kwargs['only_monthly'] if 'only_monthly' in kwargs else False
        
        files = func(*args, **kwargs)
        
        if not only_monthly:
            files.daily.to_csv(files.daily_path, index=False)
        
        if save_monthly or only_monthly:
            files.monthly.to_csv(files.monthly_path, index=False)

        return Response(status_code=status.HTTP_204_NO_CONTENT)

    return wraps
        
def CreateAttendence(total_year: int, course_alias: str):
    path = Path("repository/AttendenceFiles")
    path.mkdir(exist_ok=True)
    
    for i in range(1, total_year + 1):
        attendence = pd.DataFrame(columns = ['StudentsName'])
        monthly_report = pd.DataFrame(columns=['StudentsName'])
        attendence.to_csv(f"repository/AttendenceFiles/{course_alias}{i}.csv", index=False)
        monthly_report.to_csv(f"repository/AttendenceFiles/{course_alias}{i}_monthly.csv", index=False)

# Functions

@save_files
@get_attendence_files
def admit_students(request: Schemas.AddStudent, files: Schemas.Files, **kwargs):
    '''kwargs: open_files(default) = True'''
    
    full_names = files.daily['StudentsName'].to_list()+[request.name]
    files.daily = pd.DataFrame(data = full_names, columns=files.daily.columns)
    files.monthly = pd.DataFrame(data = full_names, columns=files.daily.columns)
    
    return files

@get_attendence_files
def get_student_names(request: Schemas.set_class, files: Schemas.Files, **kwargs):
    names = files.daily['StudentsName'].to_list()
    if not len(names):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return Schemas.students_attendence(names=names)

@save_files
@get_attendence_files
def take_attendence(request: Schemas.TakeAttendence, files: Schemas.Files, **kwargs):
    '''
    kwargs open_daily(default) = False, this will only open daily attendence file
    '''
    df = files.daily
    attendence = df[request.date].values if request.date in df else np.zeros(len(df))
    present_indices = df['StudentsName'][df['StudentsName'].isin(request.present)].index
    
    if request.take_full_day == True:
        assert not attendence.any(),\
            f"{request.date} attendence already taken"
        attendence[present_indices] = 1.
        
    else: attendence[present_indices] += .20

    files.daily[request.date] = attendence

    return files
