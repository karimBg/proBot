import datetime

from repository.data_access import cursor


# Creates a list out of all existing jobs for a specific user.
def list_jobs(user_id,role_id):
   if(role_id==100):
      query =f"SELECT JobRef,Title FROM jobs WHERE IdUserDb='{user_id}'"
   else:
      query =f"SELECT JobRef,Title FROM jobs WHERE IdUserDb='{user_id}' And Role={role_id}"

   jobs = cursor.execute(query)
   possible_jobs = []
   for row in jobs:
      possible_jobs.append(
         {"jobRef": row[0],
         "jobTitle": row[1]}
      )
   
   return possible_jobs

result= list_jobs("189c6a81-abde-4388-a757-a50da959e8da",2)
print(result)
def generate_job_buttons(possible_jobs):
   buttons = []
   for job in possible_jobs:
      ref=job["jobRef"]
      title = job["jobTitle"]
      payload = job["jobRef"]
      buttons.append({ "title": ref+"\n"+title, "payload": payload })
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
def get_job_data(job_option, JobRef, user_id):
   job_option = transform_option(job_option)
   query = cursor.execute(f"SELECT {job_option.capitalize()} FROM jobs WHERE JobRef='{JobRef}' AND IdUserDb='{user_id}'")

   job_data = ""
   for row in query:
      job_data = row[0]

   if(type(job_data) is datetime.datetime):
      return job_data.strftime(f'''%d/%m/%Y''')

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