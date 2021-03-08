import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="testUser",
  password="b212"
)

mycursor = mydb.cursor()

mycursor.execute("CREATE DATABASE mydatabase")
