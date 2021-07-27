import pandas as pd

def CreateAttendence(total_year: int, course_alias: str):
    for i in range(1, total_year + 1):
        attendence = pd.DataFrame(columns = ['StudentsName'])
        monthly_report = pd.DataFrame(columns=['StudentsName'])
        attendence.to_csv(f"repository/AttendenceFiles/{course_alias}{i}.csv", index=False)
        monthly_report.to_csv(f"repository/AttendenceFiles/{course_alias}{i}_monthly.csv", index=False)

