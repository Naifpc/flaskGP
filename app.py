from flask import Flask, render_template, url_for, request, redirect,session
#import sqlalchemy
from datetime import timedelta



app = Flask(__name__)
app.secret_key = "graduate"
app.permanent_session_lifetime = timedelta(days=1) #keep session for one day

@app.route("/")
def index():
    return render_template("login.html")  # Go to login by default

@app.route("/login", methods=["POST","GET"])
def login():
    if request.method == "POST":
        user = request.form["username"]
        password = request.form["password"]
        session["user"]=user
        session["password"]=password # get username and password and save in session then go to dashboard
        return redirect(url_for("dashboard"))
    else:
        if "user" in session:
           return redirect(url_for("dashboard")) #if user already in Session go to Dashboared
        return render_template("login.html") 

@app.route("/dashboard")
def dashboard():
    if "user" in session: 
        user = session["user"]
        return render_template("dashboard.html",username = user)
    else:
        return redirect(url_for("login"))

@app.route("/registerdUsers")
def registerdUsers():
    return render_template("registerdUsers.html")

@app.route("/history")
def history():
    return render_template("history.html")

@app.route("/newUser")
def newUser():
    return render_template("newUser.html")

@app.route("/logout") #Delete username and password from Session then go to login
def logout():
    session.pop("user",None)
    session.pop("password",None)
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)