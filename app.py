from flask import Flask,redirect, url_for, render_template, request, redirect, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, MetaData, Table, insert
import os

app = Flask(__name__)
app.secret_key = "@00admin185@"

app.config["IMAGE-UPLOADS"] = './static/images/uploads'

ENV='production'

if ENV == 'development':
    app.config['SQLALCHEMY_DATABASE_URL'] = 'postgresql://postgres:@Rosewood185@localhost/postgres'
    app.config['SQLALCHEMY_BINDS'] = {
    'alogin': 'postgresql://postgres:@Rosewood185@localhost/alogin',
    'graphics':'postgresql://postgres:@Rosewood185@localhost/graphics',
    'contact':'postgresql://postgres:@Rosewood185@localhost/contact'
}
else:
    app.config['SQLALCHEMY_DATABASE_URL'] = 'postgres://lwrajfomnlvqot:e5bc5616ef4488c3067bcebfb0cd0b38e1f31cb72b1edc49572f3508f26880c6@ec2-34-203-255-149.compute-1.amazonaws.com:5432/d6qliq3jlf1nir'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class ALogin(db.Model):
    __bind_key__ = 'alogin'
    _id = db.Column("id", db.Integer, primary_key = True)
    username = db.Column("username", db.String(15))
    password = db.Column("password", db.String(15))

    def __init__(self, username, password):
        self.username = username
        self.password = password

class Contact(db.Model):
    __bind_key__ = 'contact'
    _id = db.Column("id", db.Integer, primary_key = True)
    name = db.Column("name", db.String(30))
    phone = db.Column("phone", db.String(14))
    email = db.Column("email", db.String(30))
    message = db.Column("message", db.String(150))
    
    def __init__(self, name, phone, email, message):
        self.name = name
        self.phone = phone
        self.email = email
        self.message = message

class Graphics(db.Model):
    __bind_key__ = 'graphics'
    _id = db.Column("id", db.Integer, primary_key = True)
    filename = db.Column("filename", db.String(15))
    title = db.Column("title", db.String(30))
    description = db.Column("description", db.String(50))
    url = db.Column("url", db.String(30))
    width = db.Column("width", db.String(10))
    height = db.Column("height", db.String(10))

    def __init__(self, filename, title, description, url, width, height):
        self.filename = filename
        self.title = title
        self.description = description
        self.url = url
        self.width = width
        self.height = height

db.create_all()
    
@app.route("/", methods=['POST', 'GET'])
def inquiry1():
    if request.method == 'POST':
        """Store Inquiry Form In Database"""
        inquiry = Contact(request.form['name'], request.form['phone'], request.form['email'], request.form['message'])
        db.session.add(inquiry)
        db.session.commit()
        session.permanent = True
        flash("Inquiry Submitted Successfully!", "info")
        return redirect(url_for('inquiry1'))
    else:
        return render_template("index.html")

@app.route("/admin-login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form["username"] == "admin" and request.form["password"] == "password":
            session['admin'] = request.form['username']
            return redirect(url_for('inquiry2'))
        if request.form["username"] != "admin" and request.form["password"] != "password":
            flash("Credentials Submitted Incorrectly*")
    return render_template("adminlogin.html")

@app.route("/admin-panel", methods=['POST', 'GET'])
def inquiry2():
    if 'admin' not in session:
        return redirect(url_for('login'))

    else:
        """Query All Data from Inquiry Form in Database"""
        info = Contact.query.all()
        db.session.commit()
        session.permanent = True
        return render_template("admin.html", info=info)  

        if request.method == 'POST':
            """Retrieve Each Individual Data Entry (To Display)"""
            inquiry = Contact(request.form['name'], request.form['phone'], request.form['email'], request.form['message'])
            db.session.add(inquiry)
            db.session.commit()
            session.permanent = True
            return redirect(url_for('inquiry1'))
        else:
            return render_template("index.html")

@app.route("/logout", methods=['POST', 'GET'])
def logout():
    session.pop("admin", None)
    return redirect(url_for('login'))

@app.route("/delete/<int:_id>", methods=['POST', 'GET'])
def delete(_id):
    if request.method == 'POST':
        """Query Each Form Submission By ID (To Delete)"""
        data = Contact.query.get(_id)
        db.session.delete(data)
        db.session.commit()
        session.permanent = True
        return redirect("/admin-panel")
    else:
        return redirect("/admin-panel")

@app.route("/admin-panel/upload", methods=['POST', 'GET'])
def graphics1():
    if request.method == 'POST':
        design = Graphics(request.form['filename'], request.form['title'], request.form['description'], request.form['url'], request.form['width'], request.form['height'])
        db.session.add(design)
        db.session.commit()
        session.permanent = True

        if request.files:
            image = request.files["image"]
            image.save(os.path.join(app.config["IMAGE-UPLOADS"], image.filename))
            
        return redirect(url_for('graphics1'))
    else:
        return render_template("admin.html")

@app.route("/uploads", methods=['POST', 'GET'])
def graphics2():
    app.config["IMAGE-UPLOADS"] = './static/images/uploads'
    
    data = Graphics.query.all()
    db.session.commit()
    session.permanent = True
    return render_template("graphics.html", data=data)  

    if request.method == 'POST':
        design = Graphics(request.form['filename'], request.form['title'], request.form['description'], request.form['url'], request.form['width'], request.form['height'])
        db.session.add(design)
        db.session.commit()
        session.permanent = True
        return redirect(url_for('graphics1'))
    else:
        return render_template("admin.html")

if __name__ == "__main__":
    app.run()