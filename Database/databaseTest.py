import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="testUser",
  password="b212"
)

mycursor = mydb.cursor()

mycursor.execute("INSERT INTO test.testtable VALUES (7, 8, 9, 10, 11);")
mycursor.execute("COMMIT;")