import sqlite3
import os
import hashlib
import json

def createTable(json) -> bool:
    if not os.path.exists(f"{os.getcwd()}/trucks.db"):
        
        if not createTrucks(json): print("Error in `createTrucks(json)`"); exit(1)
        if not createUsers(): print("Error in `createUsers()`"); exit(1)
        if not createRatings(): print("Error in `createRatings()`"); exit(1)

        return True
    else:
        return False

###################################### Define Trucks ########################################

def createTrucks(json) -> bool:
    """
    Defines database,
    should only be called from root directory.
    """
    
    conn = sqlite3.connect("trucks.db")
    
    conn.cursor().execute("""\
        CREATE TABLE IF NOT EXISTS trucks(
            ID INTEGER UNIQUE,
            NAME CHAR(32) UNIQUE,
            CATEGORY CHAR(32),
            BIO CHAR(256),
            EXAMPLE_IMG CHAR(128),
            COVER_IMG CHAR(128),
            WEBSITE CHAR(64),
            FACEBOOK CHAR(128),
            INSTAGRAM CHAR(128),
            TWITTER CHAR(128),
            
            PRIMARY KEY(ID)
        );
    """)
    conn.commit()

    if loadTrucks(json) == False:
        return False
    
    return True

def updateTrucks(json) -> bool:
    """
    Updates api resultant in the database.
    """

    conn = sqlite3.connect("trucks.db")

    conn.cursor().execute("DROP TABLE trucks")

    conn.commit()

    return createTrucks(json)

def loadTrucks(json) -> bool:
    """
    Loads api resultant into the database.
    """

    query = "INSERT INTO trucks VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"

    conn = sqlite3.connect("trucks.db")
    try:
        for entry in json:
            #print(entry["avatar"]["src"])
            conn.cursor().execute(query,(
                entry["truck_id"],
                entry["name"],
                entry["category"],
                entry["bio"],
                entry["avatar"]["src"],
                entry["cover_photo"]["src"] if isinstance(entry["cover_photo"], dict) else '',
                entry["website"],
                entry["facebook_url"],
                entry["instagram_handle"],
                entry["twitter_handle"]
                )                  
            )

        conn.commit()
        return True
    except Exception as e: # what ?????
        #print("Error, ", e)
        #return 1
        return False

def depreciated_Truck_example(numOf: int) -> list:
    conn = sqlite3.connect("trucks.db")

    return conn.cursor().execute(
        f"SELECT * FROM trucks ORDER BY RANDOM() LIMIT {numOf}"
    ).fetchall()

def truck_example(numOf: int) -> str:
    if numOf > 1:
        exit()

    conn = sqlite3.connect("trucks.db")
     
    cursor = conn.cursor()

    truck = cursor.execute(
        f"SELECT * FROM trucks ORDER BY RANDOM() LIMIT {numOf}"
    ).fetchall()
     

    out = dict(zip([column[0] for column in cursor.description], truck))
    tID = out["ID"][0]
    rating = cursor.execute(f"SELECT AVG(SCORE) as a_s FROM ratings where TRUCK = '{tID}'").fetchall()

    out["rating"] = rating[0][0] 
    
    return json.dumps(out)
    
####################################### End Trucks ##########################################     

###################################### Define Users #########################################

def createUsers() -> bool:
    """
    Defines users database,
    should only be called from root directory.
    """
    
    conn = sqlite3.connect("trucks.db")
        
    try: # couldnt use CREATE TABLE IF NOT EXITS HERE, in order to check for table creation on attempt.
        conn.cursor().execute("""\
            CREATE TABLE users (
                UID INTEGER PRIMARY KEY AUTOINCREMENT,
                USERNAME CHAR(32) UNIQUE,
                PASSWORD CHAR(128),
                REP INTEGER,
                NUMOFRATINGS INTEGER
            );
        """)

        conn.commit()

        return True  
    except:
        #print("Exception: ", e)
        return False
    

def loadUser(username, password) -> bool:
    h = hashlib.sha256()
    h.update(password.encode())
    password = h.hexdigest()

    conn = sqlite3.connect("trucks.db")

    conn.cursor().execute("INSERT INTO users(USERNAME, PASSWORD) VALUES (?, ?)", (username, password))

    conn.commit()
    return True

def checkUser(username, password) -> bool:
    h = hashlib.sha256()
    h.update(password.encode())
    password = h.hexdigest()
    
    conn = sqlite3.connect("trucks.db")
    
    e = conn.cursor().execute(f"SELECT CASE WHEN EXISTS(SELECT * FROM users WHERE USERNAME = '{username}' AND PASSWORD = '{password}') THEN 1 ELSE 0 END as exist;").fetchall()



    if(e[0][0] == 0): return False
    else: return True

######################################## End Users ##########################################

###################################### Define Ratings #######################################

def createRatings() -> bool:
    """
    Defines ratings database,
    should only be called from root directory.
    """
    
    conn = sqlite3.connect("trucks.db")
        
    try: # couldnt use CREATE TABLE IF NOT EXITS HERE, in order to check for table creation on attempt.
        conn.cursor().execute("""\
            CREATE TABLE ratings (
                UID INTEGER PRIMARY KEY AUTOINCREMENT,
                TRUCK CHAR(32),
                SCORE INTEGER,

                FOREIGN KEY(TRUCK) REFERENCES trucks(ID)
            );
        """)

        conn.commit()

        return True  
    except:
        #print("Exception: ", e)
        return False

def loadRating(truck, score) -> bool:
    conn = sqlite3.connect("trucks.db")

    conn.cursor().execute("INSERT INTO ratings(TRUCK, SCORE) VALUES (?, ?)", (truck, score))
    # conn.cursor().execute("DELETE FROM ratings()")
    conn.commit()
    return True

def rating_example():
    conn = sqlite3.connect("trucks.db")
     
    cursor = conn.cursor()

    truck = cursor.execute(
        f"SELECT * FROM ratings"
    ).fetchall()
     

    return truck

def deleteRow(rowID):
    conn = sqlite3.connect("trucks.db")

    cursor = conn.cursor()

    truck = cursor.execute(f"DELETE FROM ratings WHERE UID={rowID}")
    
    conn.commit()
####################################### End Ratings #########################################
