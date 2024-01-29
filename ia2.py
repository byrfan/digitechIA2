from flask import *

app = Flask("IA2 Template")

@app.route("/")
def landing():
    return render_template("index.html")

app.run(host="127.0.0.1", port="5000", debug=True)
