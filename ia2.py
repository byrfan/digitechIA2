from flask import *
from dbHandler import db

print("Creating Flask Instance")
app = Flask("IA2 Template")

print("Checking DB Status... ", end="")
if not bool(db.create):
    print("Exists!")
else:
    print("DB Does Not Exist.\n New DB Created...")

@app.route("/")
def landing():
    eg = db.truck_example(8)
    return render_template("index.html", left=eg[:4], right=eg[4:])

app.run(host="127.0.0.1", port="5000", debug=True)
