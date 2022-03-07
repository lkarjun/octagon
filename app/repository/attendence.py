from fastapi import HTTPException, status, Response
import pandas as pd
import numpy as np
from pathlib import Path
from sqlalchemy import and_, or_
from sqlalchemy.orm.session import Session
from database import models
from repository import Schemas
from calendar import monthrange
from typing import Callable, Union, List
import functools

# Decorators
BASE_PATH = Path("repository/AttendenceFiles")

def get_attendence_files(func: Callable):
    
    @functools.wraps(func)    
    
    def wrap(*args, **kwargs):
        
        open_files = kwargs['open_file'] if 'open_file' in kwargs else True
        open_monthly = kwargs['open_monthly'] if 'open_monthly' in kwargs else False
    
        course, year = kwargs['request'].course, kwargs['request'].year
        daily_path = BASE_PATH/f"{course}{year}.csv"
        monthly_path = BASE_PATH/f"{course}{year}_monthly.csv"
        
        if open_files:
            try:
                daily = pd.read_csv(daily_path)
                monthly = pd.read_csv(monthly_path) if open_monthly else None
            except FileNotFoundError:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Files Not Found.")

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
        
def createFiles(year: int, course_alias: str):
    attendence = pd.DataFrame(columns = ['StudentsName'])
    monthly_report = pd.DataFrame(columns=['StudentsName'])
    attendence.to_csv(f"repository/AttendenceFiles/{course_alias}{year}.csv", index=False)
    monthly_report.to_csv(f"repository/AttendenceFiles/{course_alias}{year}_monthly.csv", index=False)

def createAttendence(total_year: int, course_alias: str):
    path = Path("repository/AttendenceFiles")
    path.mkdir(exist_ok=True)

    for i in range(1, total_year + 1): createFiles(i, course_alias)

def deleteAttendence(total_year: int, course_alias: str):
    path = Path("repository/AttendenceFiles")
    
    for i in range(1, total_year + 1):
        rem_file = path/f"{course_alias}{i}.csv"
        rem_monthly = path/f"{course_alias}{i}_monthly.csv"
        rem_file.unlink(missing_ok=True)
        rem_monthly.unlink(missing_ok=True)

# Functions

@save_files
@get_attendence_files
def admit_students(request: Schemas.AddStudent, files: Schemas.Files, **kwargs):
    '''kwargs: open_files(default) = True'''
    
    full_names = files.daily['StudentsName'].to_list()+[request.name]
    files.daily = pd.DataFrame(data = full_names, columns=files.daily.columns)
    files.monthly = pd.DataFrame(data = full_names, columns=files.monthly.columns)
    
    return files

@save_files
@get_attendence_files
def remove_students(request: Schemas.DeleteStudent, files: Schemas.Files, **kwargs):
    '''kwargs: open_files(default) = True'''
    files.daily = files.daily[files.daily['StudentsName'] != request.name].reset_index().drop('index', axis=1)
    files.monthly = files.monthly[files.monthly['StudentsName'] != request.name].reset_index().drop('index', axis=1)
    return files

@get_attendence_files
def get_student_names(request: Schemas.set_class, files: Schemas.Files, **kwargs):
    names = files.daily['StudentsName'].to_list()

    if request.date in files.daily.columns:
        a = files.daily[request.date]
        if np.any(a>=1):
            raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, 
                        detail=f"{request.date} attendence already taken")
    
    if not len(names):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return Schemas.students_attendence(names=names)

@save_files
@get_attendence_files
def take_attendence(request: Schemas.TakeAttendence, files: Schemas.Files, **kwargs):
    '''
    kwargs open_monthly(default) = False, this will only open daily attendence file
    '''
    df = files.daily
    attendence = df[request.date].values if request.date in df else np.zeros(len(df))
    present_indices = df['StudentsName'][df['StudentsName'].isin(request.present)].index
    
    if request.take_full_day == True:
        if attendence.any():
            raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, 
                        detail=f"{request.date} attendence already taken")
        # assert not attendence.any(),\
        #     f"{request.date} attendence already taken"
        attendence[present_indices] = 1.
        
    else: attendence[present_indices] += .20

    files.daily[request.date] = attendence

    return files

@get_attendence_files
def attendence_analysing(request: Schemas.Analysing, files: Schemas.Files, **kwargs):

    df = files.daily
    if request.last_month: 
        
        which_month = request.which_month
        date_columns = [date for date in df.columns[1:] if date[5:7] == which_month]
        if not len(date_columns): raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                                                detail=f"No attendence taken in {which_month} month")
        return get_analysis(df, date_columns, six_mnth=False)
    

    date_columns = df.columns.to_list()

    if not len(date_columns) - 1 : raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                                                  detail="No attendence taken in this month")
    
    return get_analysis(df, date_columns)

@get_attendence_files
def show_attendence_data(request: Schemas.ShowAttendence, files: Schemas.Files, **kwargs):
    column = files.daily.columns
    data = files.daily.round(2).values
    return column, data

@get_attendence_files
def most_absentee(request: Schemas.MostAbsentee, files: Schemas.Files, **kwargs):
    df = files.daily
    
    date_columns = df.columns.to_list()

    if not len(date_columns) - 1 : raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                                                  detail="No attendence taken in this month")
    
    number_of_working_days = df.shape[1] - 1
    number_of_working_days_left = 90 - number_of_working_days

    analysis = get_analysis(df, date_columns)
    most_absentee = analysis[analysis["PERCENTAGE"] < 75]
    there_is = len(most_absentee)
    most_absentee = zip(most_absentee["FULL_NAME"], most_absentee["PERCENTAGE"])
    
    return most_absentee, there_is, (number_of_working_days, number_of_working_days_left)

@save_files
@get_attendence_files
def attendence_correction(request: Schemas.AttendenceCorrection, files: Schemas.Files,\
                            db: Session, **kwargs):
    df = files.daily
    column = request.date
    percentage = request.percentage
    
    if column not in df.columns:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail="In this date there is no attendence taken")
    
    for name in request.names:
        index_row = df[df['StudentsName'] == name].index[0]
        current_percent = df.at[index_row, column]
        
        if current_percent <= 1.0 and (value:=current_percent+percentage) <= 1.0:
            df.at[index_row, column] = value
        else:
            df.at[index_row, column] = 1.0

        corrections = models.Corrections(
                    course = request.course, year = request.year,
                    date = request.date, student_name = name,
                    reason = request.reason, percentage = request.percentage
                )
    
        db.add(corrections)
        db.commit()
        db.refresh(corrections)
            
    return files


def remove_students_for_new_semester(request: Schemas.TerminalZone, **kwargs):
    db, user = kwargs['db'], kwargs['user']
    students_details = db.query(models.Students).filter(and_(
            models.Students.department == user.department,
            models.Students.course == request.course,
            models.Students.year == request.year
        ))
    students_details.delete(synchronize_session=False)
    db.commit()
    createFiles(request.year, request.course)


@save_files
@get_attendence_files
def promote_students(request: Schemas.TerminalZone, files: Schemas.Files, **kwargs):
    db, user = kwargs['db'], kwargs['user']
    createFiles(request.year, request.course)
    files.daily_path = f"repository/AttendenceFiles/{request.course}{request.year+1}.csv"
    files.monthly_path = f"repository/AttendenceFiles/{request.course}{request.year+1}_monthly.csv"
    files = remove_columns(files)
    students_details = db.query(models.Students).filter(and_(
            models.Students.department == user.department,
            models.Students.course == request.course,
            models.Students.year == request.year
        ))
    students_details.update({'year': request.year+1})
    db.commit()

    return files


@save_files
@get_attendence_files
def start_new_semester(request: Schemas.TerminalZone, files: Schemas.Files, **kwargs):
    return remove_columns(files)


# helper functions

def remove_columns(files: Schemas.Files) -> Schemas.Files:
    files.daily = files.daily['StudentsName']
    files.monthly = files.monthly['StudentsName']
    return files

def calculate_score(x: float):
    '''given x: float return internal mark based on condition'''
    if x >= 90: return 5
    elif x >= 85 and x <= 89: return 4
    elif x >= 80 and x <=84: return 3
    elif x >=76 and x <= 79: return 2
    elif x == 75 and x< 76: return 1
    else: return 0

def get_analysis(df: pd.DataFrame, date_columns: Union[pd.Index, List], six_mnth = True):
    
    number_of_working_days = len(date_columns)
    df_working = df[date_columns]

    present_count = df_working.sum(axis=1)
    percentage = (present_count / number_of_working_days) * 100
    
    if six_mnth:
        convert_to_90 = percentage / 90 * 100
        percentage = convert_to_90.round().to_list()

    else: percentage = percentage.round().to_list()

    students_names = df['StudentsName'].iloc[present_count.index].to_list()
    
    total_leav = np.count_nonzero(df_working==0.0, axis=1).tolist()
    
    data = {"FULL_NAME": students_names, "TOTAL_LEAVE": total_leav,
            "PERCENTAGE": percentage}
    
    final_report = pd.DataFrame(data = data,
                        columns=["FULL_NAME", "TOTAL_LEAVE", "PERCENTAGE"])
    
    final_report["INTERNAL_MARK"] = final_report["PERCENTAGE"].apply(calculate_score)
    
    return final_report