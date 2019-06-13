import datetime
import pyodbc

from repository.data_access import cursor, cnxn

def check_error(intro, error_message):
   info_data = ""
   for row in intro:
      info_data = row[0]
   if(info_data is None): 
      info_data= error_message
   return info_data

def getIntroduction(user_id):
   intro = cursor.execute(f"SELECT EntrepriseIntroduction FROM Infos WHERE IdUserDb='{user_id}'")
   info_data = check_error(intro, "Not currently available :c")
   return info_data

def getEmail(user_id):
   intro = cursor.execute(f"SELECT Email FROM Infos WHERE IdUserDb='{user_id}'")
   info_data = check_error(intro, "Not currently available :c")
   return info_data

def getPhone(user_id):
   intro = cursor.execute(f"SELECT PhoneNumber FROM Infos WHERE IdUserDb='{user_id}'")
   info_data = check_error(intro, "Not currently available :c")
   return info_data

def getLocation(user_id):
   intro = cursor.execute(f"SELECT Location FROM Infos WHERE IdUserDb='{user_id}'")
   info_data = check_error(intro, "Not currently available :c")
   return info_data
