from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class P_INFO(db.Model):
    __tablename__ = "P_INFO"
    MAIL = db.Column(db.String(100), unique=True, primary_key=True)
    PASSWORD = db.Column(db.String(100))
    #P_NAME = db.Column(db.String(100))
    #CONTACT = db.Column(db.Integer)
    SECURITY_Q=db.Column(db.String(100))
    SECURITY_ANS=db.Column(db.String(30))
    #ADDRESS = db.Column(db.String(250))
    #CITY=db.Column(db.String(100))

class H_INFO(db.Model):
    __tablename__="H_INFO"
    MAIL = db.Column(db.String(100), primary_key=True, unique=True)
    H_NAME = db.Column(db.String(100), unique=True)
    CITY = db.Column(db.String(100))
    ADDRESS = db.Column(db.String(250))
    PASSWORD = db.Column(db.String(100))
    CONTACT = db.Column(db.Integer)
    SECURITY_Q=db.Column(db.String(100))
    SECURITY_ANS=db.Column(db.String(30))

class A_INFO(db.Model):
    __tablename__="A_INFO"
    MAIL = db.Column(db.String(100),primary_key=True, unique=True, nullable=False)
    PASSWORD = db.Column(db.String(100), nullable=False)

class C_INFO(db.Model):
    __tablename__="C_INFO"
    C_ID=db.Column(db.Integer, primary_key=True,unique=True,nullable=False,autoincrement=True)
    C_NAME=db.Column(db.String(200))
    AGE=db.Column(db.Integer)
    DOB=db.Column(db.Date)
    GENDER=db.Column(db.String(100))
    BLOOD_TYPE=db.Column(db.String(100))
    P_MAIL=db.Column(db.String(100),db.ForeignKey('P_INFO.MAIL'), nullable=False)
    
class APPOINTMENT(db.Model):
    __tablename__="APPOINTMENT"
    AP_ID = db.Column(db.Integer, primary_key=True,autoincrement=True)
    C_ID=db.Column(db.Integer,db.ForeignKey('C_INFO.C_ID'),nullable=False)
    H_NAME=db.Column(db.String(100),db.ForeignKey('H_INFO.H_NAME'), nullable=False)
    DATE=db.Column(db.Date)
    V_NAME=db.Column(db.String(50))
    STATUS=db.Column(db.String(50),default="waiting for approval")

