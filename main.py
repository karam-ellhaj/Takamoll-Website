from flask import Flask, render_template, redirect,request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///Takamol.sqlite3'
db = SQLAlchemy(app)




#DONE : registring new users 


#TODO : LOGIN 
#TODO : MESSAGES(you click on the user and see the messages that he sent, the user clicks the contact us button and sees all the messages he sent or recieved)
#----------------------------------------------------------------------------------------------------------------------------------------------------------------
#TODO : adding, deleting and editing products
#----------------------------------------------------------------------------------------------------------------------------------------------------------------
#TODO : DESIGN :(

class Users(db.Model):
        id = db.Column(db.Integer, primary_key=True,nullable=False)
        email = db.Column(db.String, nullable=False)
        password = db.Column(db.Integer, nullable=False)



class Messages(db.Model):
    id = db.Column(db.Integer,primary_key=True,nullable=False)
    message = db.Column(db.String, nullable=False)
    sender = db.Column(db.Integer,nullable = False)
    reciever = db.Column(db.Integer,nullable = False)

class Messages(db.Model):
    id = db.Column(db.Integer,primary_key=True,nullable=False)
    name = db.Column(db.String, nullable=False)
    desc = db.Column(db.String,nullable = False)
    link = db.Column(db.String,nullable = False)

with app.app_context():
    db.create_all()

def ismail(email):
    try:
        email = email.split("@")
        if email[0] and email[1].split(".")[0] and email[1].split(".")[1]:
            return True
            
        return False
    except:
        return False
    

@app.route("/")
def main():
    return render_template("index.html")


@app.route("/register",methods=['POST','GET'])
def register():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        if ismail(email) and len(password)>7 :
            user = Users(email=email,password=password)
            db.session.add(user)
            db.session.commit()
        else:
            return ""
    return render_template('register.html')

@app.route("/login")
def login():pass


@app.route("/admin/users")
def users():
    users = Users.query.filter_by().all()
    return render_template("users.html",users)

if __name__ == '__main__':
    app.run(debug=True)
