from flask import Flask, render_template, redirect,request,session
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.config["SECRET_KEY"] = "secret-key" #this should be changed on deployment
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///Takamol.sqlite3' # this should be changed to the databse actual url
db = SQLAlchemy(app)

#the three classes used here are for the database
class Users(db.Model):
        id = db.Column(db.Integer, primary_key=True,nullable=False)
        email = db.Column(db.String, nullable=False)
        password = db.Column(db.Integer, nullable=False)



class Messages(db.Model):
    id = db.Column(db.Integer,primary_key=True,nullable=False)
    message = db.Column(db.String, nullable=False)
    sender = db.Column(db.Integer,nullable = False)
    reciever = db.Column(db.Integer,nullable = False)

class Products(db.Model):
    id = db.Column(db.Integer,primary_key=True,nullable=False)
    name = db.Column(db.String, nullable=False)
    desc = db.Column(db.String,nullable = False)
    link = db.Column(db.String,nullable = False)



#a function to verify if the email is correct
def ismail(email):
    try:
        email = email.split("@")
        if email[0] and email[1].split(".")[0] and email[1].split(".")[1]:
            return True
            
        return False
    except:
        return False



#the main page viewer
@app.route("/")
def main():
    return render_template("index.html")


#the signup viewer
@app.route("/register",methods=['POST','GET'])
def register():
    """
    when the user request the url 
    the function will check the method of request if it's a post request
    it means that the user submited a form
    if it a get request it means that he is request the form itself then we will return a simple html page to him

    when the user submit a form the function will check three things 
    1st is this a valid email?
    2nd is it used before?
    3rd does the confirm password equals the password
    """
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        cpass = request.form["cpass"]
        user = Users.query.filter_by(email=email).first()

        if not user and  ismail(email) and cpass == password and  len(password)>7:
            user = Users(email=email,password=password)
            db.session.add(user)
            db.session.commit()
            return redirect("/login")
        else:
            if user:
                return "المستخدم موجود بالفعل"
            elif cpass != password :
                return "كلمتا المرور ليستا متشبهتين"
            else:
                return ""
    return render_template('register.html')


#the login viewer
@app.route("/login",methods=["POST","GET"])
def login():
    """
        when the user request the url 
    the function will check the method of request if it's a post request
    it means that the user submited a form
    if it a get request it means that he is request the form itself then we will return a simple html page to him
    when the user submits a form the function will check for:
    1- does the user exists (stored in the database)
    2- is the  password stored in the database equals the one the user wrote
    """
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user = Users.query.filter_by(email = email, password=password).first()
        if user :
            session["id"] = user.id
            return redirect("/")
    return render_template("login.html")




@app.route("/about")
def about():
    return render_template("about.html")

#the page to send messages that are readable to the admin
@app.route("/contact")
def contact():
    """
    the function will check if the user logged in
    then it will check if it's get or post request
    if it's  
    post:
        the function will take the message from a form and the sender from the cookies the reciever will always be the admin (here)
        and it will redirect the user to the messages route to read the messages sent or recieved by him
    """ 
    if "id" in session:
        id = session["id"]
        if request.method == "POST":
            message = request.form["message"]
            sender = id
            reciever = "admin"
            db.session.add(Messages(message=message, reciever=reciever, sender=sender))
            db.session.commit()
            return redirect("/messages")

        messages = Messages.query.filter_by(sender=id).all()
        return render_template("contact.html",isloged_in=True)
    return render_template("contact.html",isloged_in=False)



#the design of this is not completed yet
@app.route("/messages")
def messages():
    if "id" in session:
        messages = Messages.query.filter(
           (Messages.sender == session["id"] | Messages.reciever == session["id"])
        ).all()
        return render_template("messages.html",messages = messages)




#admin-------------------------------------------------------------------------------------------------------------------------------------------------
#the design of this is not completed yet
@app.route("/admin/products")
def admin_prod():
    if "id" in session:
        admin = Users.query.filter_by(session["id"]).first() 
        if admin:
            if request.method == "POST":
                product_name = request.form["name"]
                product_desc = request.form["desc"]
                product_link = request.form["link"]
                product = Products(product_name,product_desc,product_link)
                db.session.add(product)
                db.session.commit()
        else:
            return ""
        return render_template("admin-mess.html")
    return ""



#the design of this is not completed yet
@app.route("/admin/products-update")
def prod_update():
    if request.method =="GET":
        return render_template("admin-products.html")

    old_prod = request.args["prod_id"]
    new_name = request.form["name"]
    new_link = request.form["link"]
    new_desc = request.form["desc"]

    prod = Products.query.get(old_prod)
    if prod:
        prod.name = new_name
        prod.link = new_link
        prod.desc = new_desc

    

if __name__=="__main__":
    app.run(debug=True)