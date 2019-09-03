from flask import Flask,url_for,render_template,request,redirect

from flask_sqlalchemy import SQLAlchemy

#from flask_mail import Mail

import smtplib

app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/shop'
db=SQLAlchemy(app)

#mail = Mail(app)

'''app.config.update(MAIL_SERVER = 'smtp.gmail.com',
MAIL_PORT='587',
MAIL_USE_SSL = True,
MAIL_USERNAME= 'madanlal885522@gmail.com',
MAIL_PASSWORD ='hYfkC4NvaG58r8bfPX71')'''

s = smtplib.SMTP('smtp.gmail.com',587)
s.starttls()
s.login('madanlal885522@gmail.com','hYfkC4NvaG58r8bfPX71')


class contact(db.Model):

    name = db.Column(db.String,nullable=False)
    email = db.Column(db.String,nullable=False)
    time = db.Column(db.Time,nullable=False)
    date = db.Column(db.Date,nullable=False)
    mobile = db.Column(db.Integer,nullable=False)
    messege = db.Column(db.String,nullable=False)
    serial_no = db.Column(db.Integer, primary_key=True)


@app.route('/',methods=['GET','POST'])
def index():
    if (request.method == 'POST'):
        name=request.form.get('name')
        email=request.form.get('email')
        date = request.form.get('date')
        time=request.form.get('time')
        mobile=request.form.get('mobile')
        messege=request.form.get('messege')

        entry = contact(name=name,email=email,date=date,time=time,mobile=mobile,messege=messege)
        db.session.add(entry)
        db.session.commit()


        s.sendmail(email,'madanlal885522@gmail.com','new msg from '+name+'\nemail: '+email+'\nmobile: '+mobile+'\nmessege: '+messege+'\ndate :'+date+'\ntime :'+time)

        redirect('/')


    return render_template("index.html")


app.run(debug=True)