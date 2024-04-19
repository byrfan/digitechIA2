from flask import *
from dbHandler import db
from api import api
import json

print("Creating Flask Instance")
app = Flask("IA2 Template")

print("Grabbing json from API")
json = api.get()

print("Checking DB Status... ", end="")
if not db.createTable(json):
    print("Exists!")
else:
    print("DB Does Not Exist.\n New DB Created...")

users = []

@app.route("/")
def landing():
    c = request.cookies.get("user")

    eg = db.depreciated_Truck_example(8)
    return render_template("index.html", left=eg[:4], right=eg[4:], logout=0 if c in users else 1 )

@app.route("/login")
def login():
    c = request.cookies.get("user")

    return render_template("login.html", logout=0 if c in users else 1)

@app.route("/signupMethod", methods=["GET"])
def signupMethod():
    data = request.args
    db.loadUser(data["user"], data["pwrd"]) 
    return redirect("/login")

@app.route("/loginMethod", methods=["GET"])
def loginMethod():
    data = request.args
   
    if db.checkUser(data["user"], data["pwrd"]):
        res = make_response(redirect("/"))
        res.set_cookie("user", data["user"], max_age=600*3) # 600 is 10 min
        users.append(data["user"])
        return res    
    else:
        return redirect("/")

@app.route("/logout")
def logout():
    c = request.cookies.get("user")
    res = make_response(redirect("/"))
    res.set_cookie("user", "")
    users.remove(c)

    return res

@app.route("/rate")
def rate():
    c = request.cookies.get("user")  
    if not c in users:
        res = make_response(redirect("/"))
        res.set_cookie("user", "")
        return res

    # implelment ratings

    return render_template("rate.html", logout=0 if c in users else 1)

@app.route("/nextTruck")
def nT():
    truck = db.truck_example(1)
    return render_template_string(f"{truck}")

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
