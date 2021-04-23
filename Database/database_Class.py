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

        return self.max_test_id+1

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
            self.max_id = int(i[0])+1

# Min ide er at finde test_id inde i host for at den forbliver uændret, og så ville den kunne køre value id herinde.

    def upload_to_database(self, test_id, average, time_lost, reaction_time):
        mydb = mysql.connector.connect(
            host="62.107.59.124",
            user="remote",
            password="test",
            database="bil"
        )

        self.find_max_value_id();

        mycursor = mydb.cursor()

        mycursor.execute("INSERT INTO data VALUES (%s, %s, %s, %s, %s, current_timestamp());", (self.max_id, test_id, average, time_lost, reaction_time))
        mycursor.execute("COMMIT")

        return

    def run(self, test_id, data):
        print("running: {}".format(threading.Thread.getName(self)))

        self.upload_to_database(test_id, data[0], data[1], data[2])
def main():
    db = database()
    db.start()
    print("main executed")

if __name__ == "__main__":
    main()