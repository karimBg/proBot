import pyodbc
import urllib.request

cnxn = pyodbc.connect(
    "Driver={SQL Server Native Client 11.0};"
    "Server=(localdb)\\MSSQLLocalDB;"
    "Database=BackEndDb;"
    "Trusted_Connection=yes;"
)

cursor = cnxn.cursor()

# # query 1:
# response = cursor.execute(f"SELECT Title FROM jobs WHERE IdUserDb='5587499e-a518-4303-946c-cc9fc96b5bba'")

# possible_jobs = []
# for row in response:
#     # result = "%r" % row
#     possible_jobs.append({"job_title": row[0]})

# # print(possible_jobs)
# # print(result[2 : len(result) - 4])

# description = "description"

# # query 2:
# query = cursor.execute(f"SELECT {description.capitalize()} FROM jobs WHERE Title='designer' AND IdUserDb='5587499e-a518-4303-946c-cc9fc96b5bba'")
# for row in query:
#     job_data = row[0]

# # print(job_data)

# # query 3:
# import datetime

# def db_access_option(select_option):
#     select_option = select_option.lower()
#     if(select_option == "procedure"):
#         select_option = "ApplicationProcedure"
#     elif("date" in select_option):
#         select_option = "OpeningDate"
#     elif("deadline" in select_option):
#         select_option = "ApplicationDeadline"
#     return select_option

# def execute_query_stmt(query_option, query_table):
#     stmt = f"SELECT {query_option} FROM {query_table} WHERE Title='designer' AND IdUserDb='5587499e-a518-4303-946c-cc9fc96b5bba'"
#     query = cursor.execute(stmt)
#     return query

# def query_data(query_option):
#     # If We have the words: date or deadline we format the returned value
#     if("date" in query_option.lower()) or ("deadline" in query_option.lower()):
#         query_option = db_access_option(query_option)

#         for row in execute_query_stmt(query_option, "jobs"):
#             # format the date
#             print(type(row[0]))
#             result = row[0].strftime('%d-%m-%Y')
#     else:
#         for row in execute_query_stmt(query_option.capitalize(), "jobs"):
#             # Don't format anything
#             result = row[0]
#     return result

# # query_option = db_access_option("opening date")

# # query = cursor.execute(f"SELECT {query_option} FROM jobs WHERE Title='designer' AND IdUserDb='5587499e-a518-4303-946c-cc9fc96b5bba'")

# # query_data("date")


# def list_internships(user_id):
#    internships = cursor.execute(f"SELECT Title, RefInternship FROM internships WHERE IdUserDb='{user_id}'")

#    possible_internships = []
#    for row in internships:
#       possible_internships.append({
#       "internshipRef": row[1],
#       "Internship Title": row[0]
#       })

#    return possible_internships
   
# result = list_internships("5587499e-a518-4303-946c-cc9fc96b5bba")

# print(result)

# import datetime

# userId = "5587499e-a518-4303-946c-cc9fc96b5bba"
# Experience_years = "1"
# Apply_date = datetime.datetime.now()
# # query.execute("SET IDENTITY_INSERT Applicant ON")
# query = cursor.execute(f"INSERT INTO Applicant( Name, Experience_years, Apply_date, IdUserDb) VALUES ('islem', {Experience_years}, '{Apply_date}', '{userId}')")
# cnxn.commit()

# def get_word(index):
#    word_url = "http://svnweb.freebsd.org/csrg/share/dict/words?view=co&content-type=text/plain"
#    response = urllib.request.urlopen(word_url)
#    long_txt = response.read().decode()
#    words = long_txt.splitlines()
   
#    return words[index]
# print(get_word(5))

# def get_degree(degree):
#    choice = 0
#    if(degree.lower() == "master"):
#       choice = 1
#    if(degree.lower() == "technician"):
#       choice = 2
#    if(degree.lower() == "engineering"):
#       choice == 3

#    return choice


# def list_internships(user_id, degree):
#    degree = get_degree(degree)
#    if(degree == 0):
#       internships = cursor.execute(f"SELECT Title, RefInternship FROM internships WHERE IdUserDb='{user_id}'")  
#    internships = cursor.execute(f"SELECT Title, RefInternship FROM internships WHERE IdUserDb='{user_id}' and Degree={degree}")
   
#    if not internships : 
#       return "no available internships opportunity at the moment"

#    possible_internships = []
#    for row in internships:
#       possible_internships.append(
#          {
#             "internshipRef": row[0],
#             "internshipTitle": row[1]
#          }
#       )
#    if len(possible_internships) == 0 : 
#       possible_internships =  "no available internships opportunity at the moment"

#    return possible_internships

# result = list_internships("5587499e-a518-4303-946c-cc9fc96b5bba", "engineering")
# print(result)

import datetime 

# result = internships = cursor.execute(f"SELECT Description, Technologies, Period, ExpirationDate FROM internships WHERE IdUserDb='5d9b8667-ef7e-42c2-830a-3e8d18d6e41d' and RefInternship='ref-84912'")

# for row in result:
#    description = row[0]
#    technologies = row[1]
#    period = row[2]
#    deadline = row[3]

# message = ""
# if(datetime.datetime.now() < deadline):
#    deadline = "" + deadline.strftime(f'''%d/%m/%Y''')
#    message = f" description: {description} \n technologies:{technologies}\n period: {period}\n deadline: {deadline}"

def detail_internship(ref, user_id):
   internships = cursor.execute(f"SELECT Description, Technologies, Period, ExpirationDate FROM internships WHERE IdUserDb='{user_id}' and RefInternship='{ref}'")

   for row in internships:
      description = row[0]
      technologies = row[1]
      period = row[2]
      deadline = row[3]

   message = ""
   if(datetime.datetime.now() < deadline):
      deadline = "" + deadline.strftime(f'''%d/%m/%Y''')
      message = f"description: {description} \n technologies:{technologies}\n period: {period}\n deadline: {deadline}"
   
   return message

message = detail_internship("ref-84912", "5d9b8667-ef7e-42c2-830a-3e8d18d6e41d")
print(message)
