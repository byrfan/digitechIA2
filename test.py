from api import api
from dbHandler import db

"""
#defunctional tests
def testOne(): # test database and api functionality
    json = api.get()
    db.load(json)


def testTwo(): # test create() functionality in `db`
    json = api.get()
    print(db.createTrucks(json))

def testThree():
    json = api.get()
    if db.updateTrucks(json) == 1:
        exit(1)
"""

def testFour():
    case = db.truck_example(8)

    print(f"\n\n{case=}")
    print(f"{len(case)}")

def testFive():
    eg = db.truck_example(8)
    for x in eg[:4]:
        print(x[0])
    
    for x in eg[4:]:
        print(x[0])

def testSix():
    eg = db.truck_example(1)
    print(eg)

def testSeven():
    json = api.get()
    db.createTable(json)

#testOne()
#testTwo()
#testThree()
#testFour()
#testFive()
#testSix()
testSeven()