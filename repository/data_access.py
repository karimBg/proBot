import pyodbc

cnxn = pyodbc.connect(
   "Driver={SQL Server Native Client 11.0};"
   "Server=(localdb)\\MSSQLLocalDB;"
   "Database=BackEndDb;"
   "Trusted_Connection=yes;"
)
cursor = cnxn.cursor()