import mysql.connector
import threading


class database(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.max_test_id = 0
        self.max_id = 0

    def find_max_value_test_id(self):

        mydb = mysql.connector.connect(
            host="62.107.59.124",
            user="remote",
            password="test",
            database="bil"
        )

        mycursor = mydb.cursor()

        mycursor.execute("SELECT MAX(test_id) FROM data;")

        test = mycursor.fetchall()
        for i in test:
            self.max_test_id = int(i[0])

    def find_max_value_id(self):
        mydb = mysql.connector.connect(
            host="62.107.59.124",
            user="remote",
            password="test",
            database="bil"
        )

        mycursor = mydb.cursor()

        mycursor.execute("SELECT MAX(id) FROM data;")

        test = mycursor.fetchall()
        for i in test:
            self.max = int(i[0])



    def upload_to_database(self, test_id, average, lost, reaction_time):
        mydb = mysql.connector.connect(
            host="62.107.59.124",
            user="remote",
            password="test",
            database="bil"
        )

        mycursor = mydb.cursor()

        mycursor.execute("INSERT INTO data VALUES (%s, %s, %s, %s, %s, current_timestamp());", id, test_id, average, lost, reaction_time)
        mycursor.execute("COMMIT")

        return

    def run(self):
        print("running: {}".format(threading.Thread.getName(self)))
        self.upload_to_database(1,1,1,1)

db = database()
db.start()
print("main executed")