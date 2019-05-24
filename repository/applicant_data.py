import datetime
import pyodbc

from repository.data_access import cursor, cnxn

# cnxn = pyodbc.connect(
#     "Driver={SQL Server Native Client 11.0};"
#     "Server=(localdb)\\MSSQLLocalDB;"
#     "Database=BackEndDb;"
#     "Trusted_Connection=yes;"
# )

# cursor = cnxn.cursor()

def saveApplicantData(jobRef ,Name, Experience_years, Phone_number, Email, cv_link , IdUserDb):
    Apply_date = datetime.datetime.now()
    query = cursor.execute(f'''INSERT INTO Applicant
    ( 
        jobRef, Name, Experience_years, Phone_number, Email, cv_link, Apply_date, IdUserDb
    ) 
    VALUES 
    ('{jobRef}', '{Name}', {Experience_years}, '{Phone_number}', '{Email}', '{cv_link}', '{Apply_date}', '{IdUserDb}')
    ''')
    cnxn.commit()