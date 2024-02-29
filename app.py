from flask import Flask, render_template, url_for, request, redirect,session,send_file
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from io import BytesIO



app = Flask(__name__)
app.secret_key = "graduate"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(days=1) #keep session for one day

#databasecode
db = SQLAlchemy(app)

class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    password = db.Column(db.String(100))
    image = db.Column(db.LargeBinary)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now) 

    def __init__(self, name, password, image, created_at, updated_at):
        self.name = name
        self.password = password
        self.image = image
        self.created_at = created_at
        self.updated_at = updated_at
        

@app.route("/")
def index():
    return render_template("login.html")  # Go to login by default

@app.route("/login", methods=["POST","GET"])
def login():
    if "user" in session:
        return redirect(url_for("dashboard")) #if user already in Session go to Dashboared
    elif request.method == "POST":
        user = request.form["username"]
        passw = request.form["password"]

        if user == "admin" and passw == "admin":
            session["user"]=user  # get username and save in session then go to dashboard
            return redirect(url_for("dashboard")) #if user was found go to Dashboared
        else:
            return redirect(url_for("login"))
    else:
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
    return render_template("registerdUsers.html",values = users.query.all())

@app.route("/history")
def history():
    return render_template("history.html",values = users.query.all())
    
@app.route("/newUser",methods=["POST","GET"])
def newUser():
    if "user" not in session:
            return redirect(url_for("login")) #if user not in Session go to login
    if request.method == "POST":
        user = request.form["username"]
        file = request.files["image"]
        image= file.read()

        found_user =  users.query.filter_by(name=user).first() 
        if found_user:
            found_user.updated_at = datetime.now()
            db.session.commit()
        else:
            created_at = datetime.now()  # Provide current timestamp for created_at
            updated_at = datetime.now()  # Provide current timestamp for updated_at
            new_user = users(user, password, image, created_at, updated_at)
            db.session.add(new_user)
            db.session.commit() #if user not found then add new user to data base db
        
        return redirect(url_for("newUser"))
    else:
        return render_template("newUser.html") 

@app.route("/logout") #Delete username and password from Session then go to login
def logout():
    session.pop("user",None)
    return redirect(url_for("login"))

@app.route("/deleteUser", methods=["POST", "GET"]) #Delete username and password from db then go to registerdUserss
def deleteUser():
    if request.method == "POST":
        user = request.form["delete"]
        user_to_delete = users.query.filter_by(name=user).first()
        if user_to_delete:
            db.session.delete(user_to_delete)
            db.session.commit()
        return redirect(url_for("registerdUsers"))
    
@app.route('/download/<upload_id>')
def download(upload_id):
    upload = users.query.filter_by(_id=upload_id).first()
    return send_file(BytesIO(upload.image), mimetype='image/jpg')

@app.route("/updateAcount", methods=["POST", "GET"]) #update username and password 
def updateAcount():
    if request.method == "POST":
        new_username = request.form["username"]
        new_password = request.form["password"]

        session["user"]= new_username  # get username and save in session then go to dashboard

        username = str(new_username)
        password = str(new_password)

        session.pop("user",None)
        return redirect(url_for("login"))



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)