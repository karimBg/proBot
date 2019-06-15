import datetime

from repository.data_access import cursor


def get_degree(degree):
   choice = 0
   if(degree is None):
      choice = 0
   if(degree.lower() == "master"):
      choice = 1
   if(degree.lower() == "technician"):
      choice = 2
   if(degree.lower() == "engineering"):
      choice == 3

   return choice
   
def list_internships(user_id, degree):
   degree = get_degree(degree)
   if(degree == 0):
      internships = cursor.execute(f"SELECT Title, RefInternship FROM internships WHERE IdUserDb='{user_id}'")  
   internships = cursor.execute(f"SELECT Title, RefInternship FROM internships WHERE IdUserDb='{user_id}' and Degree={degree}")
   
   if not internships : 
      return "no available internships opportunity at the moment"

   possible_internships = []
   for row in internships:
      possible_internships.append(
         {
            "internshipRef": row[0],
            "internshipTitle": row[1]
         }
      )
   if len(possible_internships) == 0 : 
      possible_internships =  "no available internships opportunity at the moment"

   return possible_internships


def generate_internship_buttons(possible_internships):
   buttons = []
   for internship in possible_internships:
      ref = (internship["internshipRef"])
      title = (internship["internshipTitle"])
      payload_ref = (internship["internshipRef"])
      payload_title = (internship["internshipTitle"])
      buttons.append(
         {
            "title": ref + ": " + title, "payload": payload_ref + ": " + payload_title 
         }
      )
      
   return buttons