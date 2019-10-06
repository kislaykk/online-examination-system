from flask import Flask,render_template,session,url_for,session,redirect
from forms import AdminSignup,AdminLogin,AddStudent,DeleteStudent
from werkzeug.security import generate_password_hash,check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate 
import os

app=Flask('__name__')
app.config['SECRET_KEY']='hello its me'



##############################DATABASE CREATION#######################################

basedir=os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQL_TRACK_MODIFICATIONS']=False

db=SQLAlchemy(app)
Migrate(app,db)



###############################DATABASE CREATION#######################################





#################################TABLE model##########################################
class Admin(db.Model):
    __tablename__='admin'

    admin=db.Column(db.Text,primary_key=True)
    name=db.Column(db.Text)
    institute_id=db.Column(db.Integer,nullable=True)
    password=db.Column(db.Text)

    def __init__(self,admin,name,institute,password):
        self.admin=admin
        self.name=name
        self.institute_id=institute
        self.password=generate_password_hash(password)
    def check_password(self,password):
        return check_password_hash(self.password,password)

class Institute(db.Model):
    __tablename__='institute'
    iid=db.Column(db.Integer,primary_key=True)
    iname=db.Column(db.Text)
    
    def __init__(self,iname):
        self.iname=iname

class Student(db.Model):
    __tablename__='student'
    stid=db.Column(db.Integer,primary_key=True)
    sname=db.Column(db.Text)
    iid=db.Column(db.Integer)

    def __init__(self,sname,iid):
        self.sname=sname
        self.iid=iid
#################################TABLE model#####################################

@app.route('/')
def welcome():
    return render_template('welcome.html')
@app.route('/adashboard',methods=['POST','GET'])
def admindashboard():
    return render_template('admindash.html')
@app.route('/loginadmin',methods=['POST','GET'])
def logina():
    form=AdminLogin()
  
    if form.validate_on_submit():
        
        row=Admin.query.filter_by(admin=form.email_id.data).first()
        if row.check_password(form.password.data) and row is not None:
            session['admin']=row.admin
            session['iid']=row.institute_id
        
            return redirect(url_for('admindashboard'))
        else:
            return 'wrong password or account doesnt exist'
        
    return render_template('adminlogin.html',form=form)

@app.route('/addstudent',methods=['POST','GET'])
def addstudent():
    form=AddStudent()
    if form.validate_on_submit():
        sname=form.name.data
        iid=session['iid']
        sinst=Student(sname,iid)
        db.session.add(sinst)
        db.session.commit()

    return render_template('addstudent.html',form=form)

@app.route('/deletestudent',methods=['POST','GET'])
def deletestudent():
    form=DeleteStudent()
    if form.validate_on_submit():
        id=form.id.data
        del_st=Student.query.get(id)
        if del_st is not None:
            db.session.delete(del_st)
            db.session.commit()
        else:
            return 'data does\'nt exists'

    return render_template('deletestudent.html',form=form)
@app.route('/studentlist')
def studentlist():
    slist=Student.query.filter_by(iid=session['iid'])
    print(slist[0])
    return render_template('studentlist.html',slist=slist)
@app.route('/logouta')
def logouta():
    if 'admin' in session:
        session.pop('admin',None)
        session.pop('iid',None)
        return redirect(url_for('welcome'))
    else:
        return 'you must sign in first'
@app.route('/loginstudent')
def studentl():
    return render_template('studentlogin.html')


@app.route('/signupadmin',methods=['POST','GET'])
def adminu():
    form=AdminSignup()
    if form.validate_on_submit():
        admin=form.admin_name.data
        email=form.email_id.data
        institute=form.institute.data
        passw=form.password.data
        if passw==form.rpassword.data:
            inst=Institute(institute)
            db.session.add(inst)
            db.session.commit()
            inst=Institute.query.filter_by(iname=institute)
            
            instid=inst[0].iid
            adminstrator=Admin(email,admin,instid,passw)
            db.session.add(adminstrator)
            db.session.commit()
            return render_template('message.html',message='Succesful signup!')

        
    return render_template('adminsignup.html',form=form)

if __name__=='__main__':
    app.run(debug=True)


