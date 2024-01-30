import sqlite3
import os

def create(json) -> bool:
    """
    Creates database,
    should only be called from root directory.
    """
    if not os.path.exists(f"{os.getcwd()}/trucks.db"):
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

        if load(json) == 1:
            exit(1)
    else: 
        return 1

def update():
    pass

def load(json) -> bool:
    """
    Loads api resulant into the database.
    """

    query = "INSERT INTO trucks VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"

    conn = sqlite3.connect("trucks.db")

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