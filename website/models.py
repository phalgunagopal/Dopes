from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Domain(db.Model):
    id =db.Column(db.Integer,primary_key=True)
    domainname=db.Column(db.String(50))
    

class Repository(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(50))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    access=db.Column(db.String(3))
    creator=db.Column(db.String(150))
    commits=db.relationship('Commit')
    projects=db.relationship('Project')

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    username =db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150))
    firstname = db.Column(db.String(150))
    lastname = db.Column(db.String(150))
    repositories=db.relationship('Repository')
    commits=db.relationship('Commit')

class Project(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    
    filename = db.Column(db.String(50))
    data = db.Column(db.LargeBinary)
    repo_id=db.Column(db.Integer, db.ForeignKey('repository.id'))
    commits=db.relationship('Commit')
    
    
    
class Commit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(50))
    data = db.Column(db.LargeBinary)
    timestamp = db.Column(db.DateTime(timezone=True), default=func.now())
    comment=db.Column(db.String(300))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    project_id=db.Column(db.Integer,db.ForeignKey('project.id'))
    repo_id=db.Column(db.Integer, db.ForeignKey('repository.id'))

class Joined(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    repo_id=db.Column(db.String(10))
    user_email=db.Column(db.String(150))
    user_id=db.Column(db.Integer)


