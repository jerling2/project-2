import sqlite3
import os
from RMPUser import create_dict_profs
"""
This manager can be used to modify our db.sqlite3 database. It creates a table called professors and then
appends some data acquired from Rate My Professors. The list prof_names determines the professors that will
be added to our database. We can add names that match the RMP names to ensure proper retrieval of data. This
should be run on the nightly reset to update our data.
"""
# Get the absolute path of the current file
current_file_path = os.path.abspath(__file__)

# Get the directory containing the current file
current_directory = os.path.dirname(current_file_path)

# Navigate two directories up
two_directories_up = os.path.abspath(os.path.join(current_directory, "../../"))

# Construct the relative path to the database file
database_path = os.path.join(two_directories_up, "db.sqlite3")

# Connect to the database using the relative path
conn = sqlite3.connect(database_path)

cur = conn.cursor()

try:
        #Attempt to create a table it may exist which is fine.
        cur.execute('CREATE TABLE professors (name TEXT, difficulty INTEGER, rating INTEGER,\
            numRatings INTEGER, department TEXT, wouldTakeAgainPercent INT)')
except:

        prof_names = ["Hank Childs", "Zena Ariola", "Jee Choi", "Phil Colbert", "Dejing Dou", "Brittany Erickson"]
        new_prof_names = []

        for prof in prof_names:
                #Check if this professor has already been added to the table
                cur.execute("SELECT EXISTS (SELECT 1 FROM professors WHERE name='"+prof+"')")
                found = cur.fetchall()[0][0]
                #If they have been found then continue
                if (found == 1):
                        print("professor " + prof + " is already in the table.")
                        continue
                #Otherwise append the name that needs to be added to table
                else:
                        new_prof_names.append(prof)
        
        prof_dict = {}

        if len(new_prof_names) != 0:
                prof_dict = create_dict_profs(new_prof_names)

        for prof in prof_dict:
                #Add the information to the table for this professor
                cur.execute('INSERT INTO professors (name, difficulty, rating, numRatings, department, wouldTakeAgainPercent) VALUES (?, ?, ?, ?, ?, ?)', (prof, prof_dict[prof]["difficulty"], \
                prof_dict[prof]["rating"], prof_dict[prof]["numRatings"], prof_dict[prof]["department"], prof_dict[prof]["wouldTakeAgainPercent"] \
                ))
                conn.commit()

        cur.execute('DELETE FROM professors WHERE rowid NOT IN (SELECT min(rowid) FROM professors GROUP BY name)')
        conn.commit()

        #cur.execute('DELETE FROM professors WHERE name="Randy Harris"')
        #conn.commit()

        cur.execute("SELECT * FROM professors")
        data = cur.fetchall()
        print(data)

        

