import datetime

from repository.data_access import cursor


# Creates a list out of all existing jobs for a specific user.
def list_jobs(user_id):
   jobs = cursor.execute(f"SELECT Title FROM jobs WHERE IdUserDb='{user_id}'")

   possible_jobs = []
   for row in jobs:
      possible_jobs.append({"job_title": row[0]})
   
   return possible_jobs


def generate_job_buttons(possible_jobs):
   buttons = []
   for job in possible_jobs:
      title = (job["job_title"])
      payload = (job["job_title"])
      buttons.append({ "title": title, "payload": payload })
      
   return buttons


#  transforms an option specified by the user to one we can query the DB with.
def transform_option(select_option):
   if(select_option == "procedure"):
      select_option = "ApplicationProcedure"
   elif(select_option == "mission"):
      select_option = "Responsibilities"
   elif(select_option == "date"):
      select_option = "OpeningDate"
   elif(select_option == "deadline"):
      select_option = "ApplicationDeadline"

   return select_option


# Gets all the data for a specific job and a specific option.
def get_job_data(job_option, job_title, user_id):
   job_option = transform_option(job_option)
   query = cursor.execute(f"SELECT {job_option.capitalize()} FROM jobs WHERE Title='{job_title}' AND IdUserDb='{user_id}'")

   for row in query:
      job_data = row[0]

   if(type(job_data) is datetime.datetime):
      return job_data.strftime('%d/%m/%Y')

   return job_data

   
def getRoleID(sub_role):
   i =100
   if(sub_role=="Network and Security"):
      i=8
   elif(sub_role=="Product Marketing"):
      i=7
   elif(sub_role=="Digital Marketing"):
      i=3
   elif(sub_role=="Back-End Development"):
      i=1
   elif(sub_role=="Front-End Development"):
      i=0
   elif(sub_role=="Fullstack"):
      i=2
   if(sub_role=="UI"):
      i=4
   elif(sub_role=="UX"):
      i=5
   elif(sub_role=="UI/UX"):
      i=6
   return i 