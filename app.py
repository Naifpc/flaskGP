from flask import Flask, render_template,url_for

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("dashboard.html") #go to dashboard by default

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

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