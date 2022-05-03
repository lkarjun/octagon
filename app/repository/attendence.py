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
import sqlite3

# Decorators
BASE_PATH = Path("repository/AttendenceFiles")
ATPATH = Path("database/attendence.db")

def FULL_DATA_QUERY(course: str, year: int):
    table_name = f'{course.upper()}year{year}'
    query = f"select * from {table_name}"
    return query, table_name

#=========================Changing v2.0==============================

def get_sql_connection(func: Callable):
    @functools.wraps(func)
    def wrap(*args, **kwargs):
        connection = sqlite3.connect(ATPATH)
        func_returns = func(*args, **kwargs, sql_conn=connection)
        connection.close()
        return func_returns
    return wrap

@get_sql_connection
def get_table_names(sql_conn: sqlite3.Connection):
    cursor = sql_conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    return cursor.fetchall()

#=======================================================

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

#==========================Changing v2.0=============================

def save_df_to_db(sql_conn: sqlite3.Connection, table_name: str, 
                  df: pd.DataFrame, **kwargs):
    index = False if 'index' not in kwargs else kwargs['index']
    if_exists = 'replace' if 'if_exists' not in kwargs else kwargs['if_exists']
    try:
        df.to_sql(table_name, sql_conn,
                  index = index, if_exists = if_exists)
        return True
    except Exception as e:
        return e

@get_sql_connection
def get_db_to_df(sql_conn: sqlite3.Connection, *args, **kwargs):
    if 'query' not in kwargs:
        raise HTTPException(status_code=status.HTTP_304_NOT_MODIFIED)
    query = kwargs['query']
    try:
        df = pd.read_sql(query, sql_conn).dropna()
        return df
    except Exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Files Not Found.")
    

@get_sql_connection
def createAttendenceFile(course: str, year: int, sql_conn: sqlite3.Connection, **kwargs):
    table_name = f"{course.upper()}year{year}"
    df = pd.DataFrame(columns=['ST_ID', 'ST_NAME', 'ST_STATUS'])
    status_ = save_df_to_db(sql_conn, table_name, df,
                            **kwargs)
    if status_ == True:
        return status_
    raise HTTPException(status_code=status.HTTP_304_NOT_MODIFIED,
                            detail=f'Failed to create files: Exception {status}')

## Attendence Files Create based on duration
def createAttendenceFiles(total_year: int, course: str):
    for year in range(1, total_year + 1): createAttendenceFile(course, year, if_exists = 'replace')

## Attendence Files Deleted based on duration
@get_sql_connection
def deleteAttendenceFiles(total_year: int, course: str, sql_conn: sqlite3.Connection):
    cursor = sql_conn.cursor()
    for year in range(1, total_year + 1):
        table_name = f"{course.upper()}year{year}"
        query = f"Drop TABLE {table_name}"
        cursor.execute(query)
        sql_conn.commit()
    return

## Start new sem
@get_sql_connection
def start_new_semester_v2(sql_conn: sqlite3.Connection, data: Schemas.TerminalZone, **kwargs):
    query, table_name = FULL_DATA_QUERY(data.course, data.year)
    df = get_db_to_df(query=query)
    df = df[['ST_ID', 'ST_NAME', 'ST_STATUS']]
    sql_conn.execute(f"Drop table {table_name}")
    sql_conn.commit()

    status_ = save_df_to_db(sql_conn, table_name, df, **kwargs)
    if status_ == True:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=status.HTTP_304_NOT_MODIFIED,
                            detail=f'Failed to remove files: Exception {status_}')

## remove students when the course is over...
@get_sql_connection
def remove_students_for_new_semester_v2(sql_conn: sqlite3.Connection, request: Schemas.TerminalZone, **kwargs):
    db, user = kwargs['db'], kwargs['user']
    students_details = db.query(models.Students).filter(and_(
            models.Students.department == user.department,
            models.Students.course == request.course,
            models.Students.year == request.year
        ))
    students_details.delete(synchronize_session=False)
    db.commit()
    query, table_name = FULL_DATA_QUERY(request.course, request.year)
    sql_conn.execute(f"Drop table {table_name}")
    sql_conn.commit()
    return createAttendenceFile(request.course, request.year)
    # createFiles(request.year, request.course)
#=======================================================

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

#==========================Changing v2.0=============================

@get_sql_connection
def admit_student_v2_0(file: pd.DataFrame, 
                        course: str, 
                        year: int, 
                        sql_conn: sqlite3.Connection,
                        **kwargs):
    
    table_name = f"{course.upper()}year{year}"
    existing_file = get_db_to_df(query = f'select * from {table_name}')
    if file['ST_ID'][0] in existing_file['ST_ID']:
        raise HTTPException(status_code=status.HTTP_304_NOT_MODIFIED,
                            detail=f'Duplicate ID Found: Exception {file["ST_ID"]}')
                            
    status_ = save_df_to_db(sql_conn, table_name, file, **kwargs)
    if status_ == True:
        return status_
    raise HTTPException(status_code=status.HTTP_304_NOT_MODIFIED,
                            detail=f'Failed to create files: Exception {status_}')

@get_sql_connection
def admit_students_from_file(data: Schemas.AdmitStudentFromFile_v2_0,
                             sql_conn: sqlite3.Connection,
                             **kwargs):
    table_name = f"{data.course.upper()}year{data.year}"
    existing_file = get_db_to_df(query = f'select * from {table_name}')
    existing_file['ST_ID'] = data.file['ST_ID']
    existing_file['ST_NAME'] = data.file['ST_NAME']
    existing_file['ST_STATUS'] = data.file['ST_STATUS']
    status_ = save_df_to_db(sql_conn, table_name, existing_file, **kwargs)
    if status_ == True:
        return status_
    raise HTTPException(status_code=status.HTTP_304_NOT_MODIFIED,
                            detail=f'Failed to create files: Exception {status_}')

@get_sql_connection
def admit_student(data: Schemas.Student_v2_0,
                  file: pd.DataFrame,
                  sql_conn: sqlite3.Connection,
                  **kwargs):
    
    table_name = f"{data.course.upper()}year{data.year}"
    existing_file = get_db_to_df(query = f'select * from {table_name}')
    if file['ST_ID'][0] in existing_file['ST_ID']:
        raise HTTPException(status_code=status.HTTP_304_NOT_MODIFIED,
                            detail=f'Duplicate ID Found: Exception {file["ST_ID"]}')
                            
    status_ = save_df_to_db(sql_conn, table_name, file, **kwargs)
    if status_ == True:
        return status_
    raise HTTPException(status_code=status.HTTP_304_NOT_MODIFIED,
                            detail=f'Failed to create files: Exception {status_}')


@get_sql_connection
def remove_students(data: Schemas.DeleteStudent,
                    sql_conn: sqlite3.Connection,
                    **kwargs):
    table_name = f"{data.course.upper()}year{data.year}"
    df = get_db_to_df(query = f'select * from {table_name}')
    df = df[df["ST_ID"] != data.unique_id]
    
    status_ = save_df_to_db(sql_conn, table_name, df, **kwargs)
    if status_ == True:
        return status_
    raise HTTPException(status_code=status.HTTP_304_NOT_MODIFIED,
                            detail=f'Failed to create files: Exception {status_}')
    return df

def get_student_names_for_status_update(data: Schemas.get_names):
    df = get_db_to_df(query = FULL_DATA_QUERY(data.course, data.year)[0])
    names = df['ST_NAME'].to_list()
    ids = df['ST_ID'].to_list()
    if not len(names):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No Students are there in course {data.course} year {data.year}")
    return Schemas.StudentsAttendence_v2_0(datas = list(zip(ids, names)))

def get_student_names(data: Schemas.set_class):
    data.date = f"{data.date[8:]}-{data.date[5:7]}-{data.date[:4]}"
    df = get_db_to_df(query = FULL_DATA_QUERY(data.course, data.year)[0])
    names = df['ST_NAME'].to_list()
    ids = df['ST_ID'].to_list()

    if not len(names):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    if data.date in df.columns:
        check_ = df[data.date]
        if np.any(check_ >= 1):
            raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, 
                        detail=f"{data.date} attendence already taken")

    return Schemas.StudentsAttendence_v2_0(datas = list(zip(ids, names)))

@get_sql_connection
def take_attendence(data: Schemas.TakeAttendence_v2_0, sql_conn: sqlite3.Connection, **kwargs):
    data.date = f"{data.date[8:]}-{data.date[5:7]}-{data.date[:4]}"
    query, table_name = FULL_DATA_QUERY(data.course, data.year)
    df = get_db_to_df(query = query)
    attendence = df[data.date].values if data.date in df else np.zeros(len(df))
    present_idx = df['ST_ID'][df['ST_ID'].isin(data.present)].index

    if attendence.max() >= 1:
        raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, 
                        detail=f"{data.date} attendence already taken")

    if data.take_full_day == True:
        if attendence.any():
            raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, 
                        detail=f"{data.date} attendence already taken")
        attendence[present_idx] = 1.
    else: attendence[present_idx] += .20
    
    df[data.date] = attendence

    status_ = save_df_to_db(sql_conn, table_name, df, **kwargs)
    if status_ == True:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=status.HTTP_304_NOT_MODIFIED,
                            detail=f'Failed to create files: Exception {status_}')

def _check_attendence_data(request: Schemas.TerminalZone):
    query, _ = FULL_DATA_QUERY(request.course, request.year)
    df = get_db_to_df(query = query)
    column = df.columns[3:][::-1]
    if len(column):
        return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = 'Not admitted students or attendence didnt taken...')

def show_attendence_data(request: Schemas.ShowAttendence):
    query, _ = FULL_DATA_QUERY(request.course, request.year)
    df = get_db_to_df(query = query)
    column = sorted(df.columns[3:][::-1], reverse=True)

    if request.month != "0" and request.month:
        which_month = request.month
        if request.month != "0":
            column = [date for date in column
                  if str(date[3:5]) == which_month]
    if not len(column):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Attendence not taken for month {request.month}")
    column = ['ST_ID', 'ST_NAME'] + column
    df = df[column].values
    return column, df

def get_students_attendence_detail(request: Schemas.ShowAttendence):
    query, _ = FULL_DATA_QUERY(request.course, request.year)
    df = get_db_to_df(query=query)
    df = df[['ST_ID', 'ST_NAME']]
    column = df.columns
    df = df.values
    return column, df

def attendence_analysing(data: Schemas.Analysing):
    df = get_db_to_df(query = FULL_DATA_QUERY(data.course, data.year)[0])
    if data.last_month:
        which_month = data.which_month
        date_columns = [date for date in df.columns[3:]
                        if date[3:5] == which_month]

        if not len(date_columns): raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                                                detail=f"No attendence taken in {which_month} month")        
        return get_analysis(df, date_columns, six_mnth = False)

    date_columns = df.columns
    if not len(date_columns) - 3 : raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                                                  detail="No attendence taken in this month")
    return get_analysis(df, date_columns)

def get_analysis(df: pd.DataFrame, date_columns: Union[pd.Index, List], six_mnth = True):
    number_of_working_days = len(date_columns)
    df_working = df[date_columns]
    
    present_count = df_working.sum(axis = 1)
    percentage = (present_count / number_of_working_days) * 100

    if six_mnth:
        convert_to_90 = percentage / 90 * 100
        percentage = convert_to_90.round().to_list()
    else: percentage = percentage.round().to_list()

    df_analysis = df[['ST_ID', 'ST_NAME', 'ST_STATUS']].iloc[present_count.index]
    total_leav = np.count_nonzero(df_working == 0.0, axis = 1)
    df_analysis['TOTAL_LEAVE'] = total_leav
    df_analysis['PERCENTAGE'] = percentage
    df_analysis['INTERNAL_MARK'] = df_analysis['PERCENTAGE'].apply(calculate_score)

    return df_analysis

def most_absentee(request: Schemas.MostAbsentee, **kwargs):
    STATUS_ = "Discontinued"
    query, _ = FULL_DATA_QUERY(course=request.course, year = request.year)
    df = get_db_to_df(query=query)
    date_columns = df.columns.to_list()
    if not len(date_columns) - 3 : raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                                                  detail="No attendence taken in this month")
    number_of_working_days = df.shape[1] - 3
    number_of_working_days_left = 90 - number_of_working_days

    analysis = get_analysis(df, date_columns)
    analysis = analysis[analysis['ST_STATUS'] != STATUS_]
    most_absentee = analysis[analysis["PERCENTAGE"] < 75]
    there_is = len(most_absentee)
    most_absentee = zip(most_absentee["ST_NAME"], most_absentee["PERCENTAGE"])
    
    return most_absentee, there_is, (number_of_working_days, number_of_working_days_left)

@get_sql_connection
def attendence_correction_v2_0(sql_conn: sqlite3.Connection, 
                               request: Schemas.AttendenceCorrection, 
                               db: Session, department: str):
    query, table_name = FULL_DATA_QUERY(course=request.course, year = request.year)
    df = get_db_to_df(query=query)
    column = request.date
    column = f"{column[8:]}-{column[5:7]}-{column[:4]}"
    percentage = request.percentage
    date_columns = df.columns.to_list()
    if column not in date_columns:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail="In this date there is no attendence taken")
        # here raise date not in the column
    for id in request.student_ids:
        index_row = df[df['ST_ID'] == id].index[0]
        current_percent = df.at[index_row, column]
        value = current_percent+percentage
        if current_percent <= 1.0 and value <= 1.0:
            df.at[index_row, column] = round(value, 1)
        else:
            df.at[index_row, column] = 1.0

    status_ = save_df_to_db(sql_conn, table_name, df, if_exists='replace')
    if status_ == False:
        raise HTTPException(status_code=status.HTTP_304_NOT_MODIFIED,
                            detail=f'Failed to create files: Exception {status_}')
    corrections_ = request.dict()
    corrections_['student_ids'] = ','.join(request.student_ids)
    corrections_['department'] = department
    corrections = models.Corrections(**corrections_)
    
    db.add(corrections)
    db.commit()
    db.refresh(corrections)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

#=======================================================

@save_files
@get_attendence_files
def remove_students(request: Schemas.DeleteStudent, files: Schemas.Files, **kwargs):
    '''kwargs: open_files(default) = True'''
    files.daily = files.daily[files.daily['StudentsName'] != request.name].reset_index().drop('index', axis=1)
    files.monthly = files.monthly[files.monthly['StudentsName'] != request.name].reset_index().drop('index', axis=1)
    return files

@get_attendence_files
def get_student_names_(request: Schemas.set_class, files: Schemas.Files, **kwargs):
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
def take_attendence_(request: Schemas.TakeAttendence, files: Schemas.Files, **kwargs):
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
def attendence_analysing_(request: Schemas.Analysing, files: Schemas.Files, **kwargs):

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
def show_attendence_data_(request: Schemas.ShowAttendence, files: Schemas.Files, **kwargs):
    column = files.daily.columns
    data = files.daily.round(2).values
    return column, data

@get_attendence_files
def most_absentee_(request: Schemas.MostAbsentee, files: Schemas.Files, **kwargs):
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

def get_analysis_(df: pd.DataFrame, date_columns: Union[pd.Index, List], six_mnth = True):
    
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