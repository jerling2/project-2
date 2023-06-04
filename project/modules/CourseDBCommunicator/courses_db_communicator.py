# ------------------------------ Module Imports ------------------------------ #
from ..GrandExchange.grand_exchange import Component
import logging
import os
import json
import sqlite3

# ------------------------------- Logger Config ------------------------------ #
logger = logging.getLogger("project")
logger.setLevel(logging.INFO)


# --------------------------- Listening on Channels -------------------------- #
DB_IN_CHANNELS = ["interval cycle"]


# --------------------------- Publishing to Channels ------------------------- #
DB_OUT_CHANNELS = ["db data"]

# --------------------------- RMP API Communicator --------------------------- #


logger = logging.getLogger("project")
logger.setLevel(logging.INFO)

class CoursesDBCommunicator(Component):
    def __init__(self):
        super().__init__()
        self.subscribe_to_channels()
        logger.info("Courses DB Communicator initalized!")

    def subscribe_to_channels(self):
        """ This is called upon initialization """
        for channel in DB_IN_CHANNELS:
            self.subscribe(channel)

    def getDatabasePath(self) -> str:
        # Get the absolute path of the current file
        current_file_path = os.path.abspath(__file__)

        # Get the directory containing the current file
        current_directory = os.path.dirname(current_file_path)

        # Navigate two directories up
        two_directories_up = os.path.abspath(os.path.join(current_directory, "../../"))

        # Construct the relative path to the database file
        database_path = os.path.join(two_directories_up, "db.sqlite3")

        return database_path
    def jsonify(self, data: list) -> json:
        """
        Converts course list data from SQLite connector into a json object
        for frontend js parsing.
        Ex:
        {
        "name": "MATH112",
        "professors": [
        "Juan Flores"
        ],
        "schedule": "mtwf",
        "time": "0900-0950"
        }
        """

        # Convert the list of tuples to a list of dictionaries
        result = []
        for item in data:
            result.append({
                'name': item[0],
                'professors': json.loads(item[1]),
                'schedule': item[2],
                'time': item[3]
            })

        # Convert the list of dictionaries to a JSON object
        json_object = json.dumps(result)
        return json_object

    def getCourses(self):
        """
        Grab courses data from the courses database table in SQLite
        """
        # get the path to the database
        database_path = self.getDatabasePath()
        # Connect to the database using the relative path
        conn = sqlite3.connect(database_path)

        cur = conn.cursor()

        cur.execute("SELECT * FROM courses")
        data = cur.fetchall()

        cur.close()
        conn.close()

        return self.jsonify(data)

    def notify(self, topic: str, message: object):
        """ This is called on when this component recieves a message """
        logging.info("Extracting Information from Rate My Professor ... ")
        courses = self.getCourses()
        logging.info("Done")
        for channel in DB_OUT_CHANNELS:
            self.publish(channel, courses)


# ----------------- Create Instance of  Course DB Communicator ----------------- #
# This will get executed when this file is imported. If this file is imported
# for a second time, this will not be executed again.
course_db_communicator = CoursesDBCommunicator()
course_db_communicator.notify('', '')
