from api import api
from dbHandler import db

def testOne(): # test database and api functionality
    json = api.get()
    db.load(json)

def testTwo(): # test create() functionality in `db`
    json = api.get()
    if db.create(json) == 1:
        exit(1)


testTwo()
#testOne()