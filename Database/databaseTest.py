import mysql.connector

mydb = mysql.connector.connect(
  host="37.97.6.138",
  user="remote",
  password="test",
  database="bil",
  port="3306"
)


test = 0;
max = 0;

mycursor = mydb.cursor()

mycursor.execute("SELECT MAX(test_id) FROM data;");

test = mycursor.fetchall()
for i in test:
  max = int(i[0])


#mycursor.execute("INSERT INTO test.testtable VALUES (7, 8, 9, 10, 11, 4, 2);")
#mycursor.execute("COMMIT;")


print(max);