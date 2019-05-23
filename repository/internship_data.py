import datetime

from repository.data_access import cursor

def list_internships(user_id):
   internships = cursor.execute(f"SELECT Title, RefInternship FROM internships WHERE IdUserDb='{user_id}'")

   possible_internships = []
   for row in internships:
      possible_internships.append(
         {
            "internshipRef": row[0],
            "internshipTitle": row[1]
         }
      )

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