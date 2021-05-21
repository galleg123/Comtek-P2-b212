import mysql.connector
import threading


class database(threading.Thread):

    def __init__(self, test_id: int, data: list):
        threading.Thread.__init__(self)
        self.max_test_id = 0
        self.max_id = 0
        self.test_id = test_id
        self.data = data

    def find_max_value_id(self):
        mydb = mysql.connector.connect(
            host="localhost",
            user="remote",
            password="test",
            database="bil"
        )

        mycursor = mydb.cursor()
#        try:
        mycursor.execute("SELECT MAX(id) FROM data;")

        test = mycursor.fetchall()
        self.max_id = int(test[0][0]) + 1
        print(self.max_id)
#        except:
#            self.max_id = 1
#            print(self.max_id)
# Min ide er at finde test_id inde i host for at den forbliver uændret, og så ville den kunne køre value id herinde.

    def upload_to_database(self, test_id, average, time_lost, reaction_time):
        mydb = mysql.connector.connect(
            host="localhost",
            user="remote",
            password="test",
            database="bil"
        )

        self.find_max_value_id();

        mycursor = mydb.cursor()

        mycursor.execute("INSERT INTO data VALUES (%s, %s, %s, %s, %s, current_timestamp());", (self.max_id, test_id, average, time_lost, reaction_time))
        mycursor.execute("COMMIT")

        return

    def run(self):
        print("running: {}".format(threading.Thread.getName(self)))

        self.upload_to_database(self.test_id, self.data[0], self.data[1], self.data[2])
def main():
    db = database(1,[1,1,1])
    db.test_id = find_max_value_test_id()
    db.start()
    print("main executed")


def find_max_value_test_id():

    mydb = mysql.connector.connect(
        host="localhost",
        user="remote",
        password="test",
        database="bil"
    )

    mycursor = mydb.cursor()
    try:
        mycursor.execute("SELECT MAX(test_id) FROM data;")

        test = mycursor.fetchall()
        for i in test:
            max_test_id = int(i[0])
    except:
        max_test_id = 0
    return max_test_id+1


if __name__ == "__main__":
    main()