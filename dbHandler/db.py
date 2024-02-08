import sqlite3
import os

def createTable(json):
    if not os.path.exists(f"{os.getcwd()}/trucks.db"):
        
        createTrucks(json)
        createUsers()
        #if not createRatings(): exit(1)
        

        #print(createTrucks(json))

        return 0
    else:
        return 1


###################################### Create Trucks ########################################

def createTrucks(json) -> bool:
    """
    Creates database,
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

    if loadTrucks(json) == 1:
        return 1
    
    return 0
    

def updateTrucks(json) -> bool:
    """
    Updates api resultant in the database.
    """

    conn = sqlite3.connect("trucks.db")

    conn.cursor().execute("DROP TABLE trucks")

    conn.commit()

    return createTrucks(json)

def loadTrucks(json) -> None:
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
        return 0
    except Exception as e:
        #print("Error, ", e)
        #return 1
        pass

def truck_example(numOf: int) -> list:
    conn = sqlite3.connect("trucks.db")

    return conn.cursor().execute(
        f"SELECT * FROM trucks ORDER BY RANDOM() LIMIT {numOf}"
    ).fetchall()

####################################### End Trucks ##########################################     

###################################### Create Users #########################################

def createUsers() -> bool:
    """
    Creates users database,
    should only be called from root directory.
    """
    
    conn = sqlite3.connect("trucks.db")
        
    try: # couldnt use CREATE TABLE IF NOT EXITS HERE, in order to check for table creation on attempt.
        conn.cursor().execute("""\
            CREATE TABLE users(
                UID INTEGER AUTOINCREMENT UNIQUE,
                USERNAME CHAR(32) UNIQUE,
                PASSWORD CHAR(128),
                REP INTEGER,
                NUMOFRATINGS INTEGER
                
                PRIMARY KEY(UID) 
            );
        """)

        conn.commit()

        return 0  
    except Exception as e:
        print("Exception: ", e)
        return 1
    

def loadUser(username, password) -> bool:
    conn = sqlite3.connect("trucks.db")

    conn.cursor().execute("INSERT INTO users(USERNAME, PASSWORD) VALUES (?, ?)", (username, password))

    conn.commit()
    return 0

######################################## End Users ##########################################

###################################### Create Ratings #######################################

####################################### End Ratings #########################################