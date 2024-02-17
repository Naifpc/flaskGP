from flask import Flask, render_template, url_for, request, redirect



app = Flask(__name__)

@app.route("/")
def index():
    return render_template("login.html")  # Go to login by default

@app.route("/login", methods=["POST","GET"])
def login():
    if request.method == "POST":
        user = request.form["username"]
        password = request.form["password"]
        return redirect(url_for("dashboard", usr=user, pw=password))
    else:
        return render_template("login.html") 

@app.route("/dashboard/<usr>/<pw>")
def dashboard(usr, pw):
    return render_template("dashboard.html", username=usr, password=pw)

@app.route("/registerdUsers")
def registerdUsers():
    return render_template("registerdUsers.html")

@app.route("/history")
def history():
    return render_template("history.html")

@app.route("/newUser")
def newUser():
    return render_template("newUser.html")


if __name__ == "__main__":
    app.run(debug=True)