from flask import Flask, request, jsonify, Response
from flask_sqlalchemy import SQLAlchemy
from faker import Faker
from random import randint, random
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://root:root@localhost:5432/store"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)    #permet d'intéragir avec la base

@app.route("/user", methods = ["POST", "GET"])
def users():
    if request.method == "GET":
        result = Users.query.all()
        userslist = []
        for row in result:
            user = {
                'id': row.id,
                'firstname': row.firstname,
                'lastname': row.lastname,
                'age': row.age,
                'email' : row.email,
                'job' : row.job
            }
            userslist.append(user)
        return jsonify(userslist)

    if request.method == "POST":
        data = request.json
        new_user = Users(
            data["firstname"],
            data["lastname"],
            data["age"],
            data["email"],
            data["job"])
        db.session.add(new_user)
        db.session.commit()
        return Response(status=200)
#def say_hello():
#    return "hello"
# Application
# need user_id
# Users: applications = db.relationship("Application")
# Application: user_id = db.Column(db.Integer, db.ForeignKey('users.id')


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    age = db.Column(db.Integer())
    email = db.Column(db.String(200))
    job = db.Column(db.String(100))
    applications = db.relationship("Application")

    def __init__(self, firstname, lastname, age, email, job):
        self.firstname = firstname
        self.lastname = lastname
        self.age = age
        self.email = email
        self.job = job

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    appname = db.Column(db.String(100))
    username = db.Column(db.String(100))
    lastconnection = db.Column(db.TIMESTAMP(timezone=True))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, appname, username, lastconnection):
        self.appname = appname
        self.username = username
        self.lastconnection = lastconnection

def populate_tables():
    for n in range(0,1000):
        #Créer tous les faux champs
        fake = Faker()
        new_user = Users(fake.first_name(), fake.last_name(), fake.pyint(0,80), fake.email(), fake.job())
        apps = ['Facebook','Instagram','Twitter','Snapchat','WhatsApp']
        nb_app = 2 #randint(1,4)
        applications = []
        for app_n in range(0, nb_app):
            app = Application(random.choice(apps),fake.user_name(),datetime.now)
            applications.append(app)
        new_user.applications = applications
        db.session.add(new_user)
    db.session.commit()

if __name__ == "__main__":  #point d'entrée de l'application
    db.drop_all()
    db.create_all()
    populate_tables()
    app.run(host="0.0.0.0", port=8080, debug=True)
