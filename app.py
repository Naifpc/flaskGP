from flask import Flask, render_template, url_for, request, redirect,session,send_file,Response,flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from io import BytesIO
import cv2
from account import *
from forms import UserForm



app = Flask(__name__)
camera=cv2.VideoCapture(0)
app.secret_key = "graduate"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(days=1) #keep session for one day

#databasecode
db = SQLAlchemy(app)

class users(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    image = db.Column(db.LargeBinary)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now) 

    def __init__(self, name, image, created_at, updated_at):
        self.name = name
        self.image = image
        self.created_at = created_at
        self.updated_at = updated_at

class entries(db.Model):
    entrie_number = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime, default=datetime.now)
    accepted= db.Column(db.Boolean, default=True)
    user_id = db.Column( db.Integer, db.ForeignKey('users.user_id'))

    def __init__(self, time):
        self.time = time
 

    


def generate_frames():
    while True:
        success,frame=camera.read() #reads camera frame
        if not success:
            break
        else:
            ret,buffer=cv2.imencode('.jpg',frame)#incode image into memory buffer
            frame=buffer.tobytes()#convert buffer to frames
        yield(b' -- frame\r\n'
                    b'Content-Type: image/jpg\r\n\r\n' + frame + b'\r\n')#we use yield instade of return becuse return will end the loop
        
current_account= account() #create instance of account


@app.route("/")
def index():
    return render_template("login.html")  # Go to login by default

@app.route("/login", methods=["POST","GET"])
def login():
    if "user" in session:
        return redirect(url_for("dashboard")) #if user already in Session go to Dashboared
    
    elif request.method == "POST":
        form = UserForm(request.form)
        if form.validate():#to validate input
            user = request.form["username"]
            passw = request.form["password"]
            if current_account.check_account(username=user, password=passw):
                session["user"]=user  # get username and save in session then go to dashboard
                flash("you have logged-in successfuly")
                return redirect(url_for("dashboard")) #if user was found go to Dashboared
            else:
                return redirect(url_for("login"))
        else:
            flash("invalid input!", 'error')
            return redirect(url_for("login"))
    else:
        return render_template("login.html") 

@app.route("/dashboard")
def dashboard():
    if "user" in session: 
        user = session["user"]
        return render_template("dashboard.html",username= user, num_of_users = users.query.count() )
    else:
        return redirect(url_for("login"))

@app.route("/registerdUsers")
def registerdUsers():
    if "user" in session: 
        return render_template("registerdUsers.html",values = users.query.all())
    else:
        return redirect(url_for("login"))

@app.route("/history")
def history():
    if "user" in session:
        return render_template("history.html",values = entries.query.all())
    else:
        return redirect(url_for("login"))
    
@app.route("/newUser",methods=["POST","GET"])
def newUser():
    if "user" in session:
        if request.method == "POST":
            form = UserForm(request.form)
            if form.validate():#to validate input
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
                    new_user = users(user, image, created_at, updated_at)
                    db.session.add(new_user)
                    db.session.commit() #if user not found then add new user to data base db
                    flash("User  have been added successfuly")
                
                return redirect(url_for("newUser"))
            else:
                flash("invalid input!", 'error')
                return redirect(url_for("newUser"))
        else:
            return render_template("newUser.html") 
    else:
        return redirect(url_for("login"))
    
@app.route("/video") 
def video():
    return Response(generate_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/logout") #Delete username from Session then go to login
def logout():
    if "user" in session:
        flash("you have been logged-out successfuly")
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
    upload = users.query.filter_by(user_id=upload_id).first()
    return send_file(BytesIO(upload.image), mimetype='image/jpg')

@app.route("/updateAcount", methods=["POST", "GET"]) #update username and password 
def updateAcount():
    if "user" in session:
        if request.method == "POST":
            form = UserForm(request.form)
            if form.validate():#to validate input
                new_username = request.form["username"]
                new_password = request.form["password"]
                current_account.update_account(username=new_username, password=new_password) #updates account info
                flash("Username and Password have been updated successfuly")
                session.pop("user",None)#exit session
                return redirect(url_for("login"))
            else:
                flash("Invalid input!", "error")
                return redirect(request.referrer)
    else:
        return redirect(url_for("login"))
            
        
        



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)