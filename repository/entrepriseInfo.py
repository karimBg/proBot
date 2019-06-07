import datetime
import pyodbc

from repository.data_access import cursor, cnxn

def getIntroduction(user_id):
   intro = cursor.execute(f"SELECT EntrepriseIntroduction FROM Infos WHERE IdUserDb='{user_id}'")
   for row in intro:
      info_data = row[0]
   return info_data

def getEmail(user_id):
   intro = cursor.execute(f"SELECT Email FROM Infos WHERE IdUserDb='{user_id}'")
   for row in intro:
      info_data = row[0]
   return info_data

def getPhone(user_id):
   intro = cursor.execute(f"SELECT PhoneNumber FROM Infos WHERE IdUserDb='{user_id}'")
   for row in intro:
      info_data = row[0]
   return info_data

def getLocation(user_id):
   intro = cursor.execute(f"SELECT Location FROM Infos WHERE IdUserDb='{user_id}'")
   for row in intro:
      info_data = row[0]
   return info_data
