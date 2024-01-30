from api import api
from dbHandler import db

"""
#defunctional test
def testOne(): # test database and api functionality
    json = api.get()
    db.load(json)
"""

def testTwo(): # test create() functionality in `db`
    json = api.get()
    if db.create(json) == 1:
        exit(1)

def testThree():
    json = api.get()
    if db.update(json) == 1:
        exit(1)

def testFour():
    case = db.truck_example(8)

    print(f"\n\n{case=}")
    print(f"{len(case)}")

#testOne()
#testTwo()
#testThree()
testFour()