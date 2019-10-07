from flask import Flask,render_template,session,url_for,session,redirect
from forms import AdminSignup,AdminLogin,AddStudent,DeleteStudent,AddPaper,AddQuestion,SeeQuestion,DeleteQuestion,DeletePaper
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

class Paper(db.Model):
    __tablename__='paper'
    pid=db.Column(db.Integer,primary_key=True)
    pname=db.Column(db.Text)
    iid=db.Column(db.Integer)
    passm=db.Column(db.Integer)
    nm=db.Column(db.Integer) #penalty marks(depends on yes or no)
    awm=db.Column(db.Integer) #awarded mark for right answer
    ques=db.relationship('Question',backref='pappers',lazy='dynamic')
    def __init__(self,pname,iid,passm,nm,awm):
        self.pname=pname
        self.iid=iid
        self.passm=passm
        self.nm=nm
        self.awm=awm

class Question(db.Model):
    __tablename__='questions'
    qid=db.Column(db.Integer,primary_key=True)
    iid=db.Column(db.Integer)
    q=db.Column(db.Text)
    a=db.Column(db.Text)
    b=db.Column(db.Text)
    c=db.Column(db.Text)
    d=db.Column(db.Text)
    ans=db.Column(db.Integer)
    pid=db.Column(db.Integer,db.ForeignKey('paper.pid'))
    def __init__(self,iid,pid,q,a,b,c,d,ans):
        self.pid=pid
        self.iid=iid
        self.q=q
        self.a=a
        self.b=b
        self.c=c
        self.d=d
        self.ans=ans


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
    if 'admin' in session:
        session.pop('admin',None)
        session.pop('iid',None)
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
@app.route('/addpaper',methods=['POST','GET'])
def addpaper():
    form=AddPaper()
    if form.validate_on_submit():
        papinst=Paper(form.pname.data,session['iid'],int(form.passm.data),int(form.nm.data),int(form.awm.data))
        db.session.add(papinst)
        db.session.commit()
    return render_template('addpaper.html',form=form)
@app.route('/addq',methods=['GET','POST'])
def addquestion():
    form=AddQuestion()
    if form.validate_on_submit():
        q=form.question.data
        pid=form.pid.data
        a=form.optionA.data
        b=form.optionB.data
        c=form.optionC.data
        d=form.optionD.data
        ans=form.rightanswer.data
        if Paper.query.get(pid) is not None:
            qformed=Question(session['iid'],pid,q,a,b,c,d,ans)
            db.session.add(qformed)
            db.session.commit()
        else:
            return 'paper not found'
    return render_template('addquestions.html',form=form)
@app.route('/seepapers')
def seepapers():
    pap=Paper.query.filter_by(iid=session['iid'])
    if pap is None:
        return 'No paper exists'
    return render_template('seepapers.html',pap=pap)

@app.route('/deletequestions',methods=['POST','GET'])
def deletequestions():
    form=DeleteQuestion()
    if form.validate_on_submit():
        qid=form.qid.data
        qu=Question.query.get(qid)
        if qu is None:
            return 'question doesnt exist'
        else:
            if session['iid']==qu.iid:
                db.session.delete(qu)
                db.session.commit()
            else:
                return 'bad input'
    return render_template('deletequestion.html',form=form)

@app.route('/seequestions',methods=['POST','GET'])
def seequestions():
    qus=None
    form=SeeQuestion()
    if form.validate_on_submit():
        pid=form.pid.data
        qus=Question.query.filter_by(pid=pid,iid=session['iid'])
        return render_template('seequestionlist.html',qus=qus)
    return render_template('seequestions.html',form=form)

@app.route('/deletepaper',methods=['POST','GET'])
def deletepaper():
    form=DeletePaper()
    if form.validate_on_submit():
        pid=form.pid.data
        qus=Question.query.filter_by(pid=pid,iid=session['iid'])
        
        pap=Paper.query.get(pid)
        if pap.iid==session['iid']:
            for j in qus:
                db.session.delete(j)
            db.session.delete(pap)
            
            db.session.commit()
    return render_template('deletepaper.html',form=form)

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


