from flask import Flask,url_for,render_template,request,session,redirect,flash
from flask_sqlalchemy import SQLAlchemy
#from flask_mail import Mail
from datetime import datetime
import os

import smtplib

app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://admin:madan12!@database-1.ccjzdhmdjmgi.us-east-1.rds.amazonaws.com/db1'

db=SQLAlchemy(app)
app.secret_key='hYfkC4NvaG58r8bfPX71'

app.config['UPLOAD_FOLDER']='C:\\uploads'

'''mail=Mail(app)
app.config.update(
MAIL_SERVER = 'smtp.gmail.com',
MAIL_PORT='465',
MAIL_USE_SSL = True,
MAIL_USERNAME= 'madanlal885522@gmail.com',
MAIL_PASSWORD ='hYfkC4NvaG58r8bfPX71')'''

username = 'admin'
password = 'madan12!'


class contacts(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(80),nullable=False)
    email = db.Column(db.String(80),nullable=False)
    phone = db.Column(db.String(80),nullable=False)
    msg = db.Column(db.String(200),nullable=False)

class posts(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(50),nullable=True)
    content=db.Column(db.String(2000),nullable=False)
    slug=db.Column(db.String(25),nullable=False)
    #date = db.Column(db.String(12), nullable=True)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/contact',methods = ['GET','POST'])
def contact():
    if (request.method=='POST'):
        name=request.form.get('_name')
        email=request.form.get('_email')
        phone=request.form.get('_phone')
        message=request.form.get('message')

        entry = contacts(name=name,email=email,phone=phone,msg=message)

        db.session.add(entry)
        db.session.commit()

    #    mail.send_message('new msg form ' + name ,sender=email,recipients=['madanlal885522@gmail.com'],body=message)

    return render_template("contact.html")

@app.route('/blog-home',methods=['GET'])
def blog_home():
    post_=posts.query.filter_by().all()
    return render_template('blog-home.html',_post=post_)

@app.route('/blog/<string:blog_slug>',methods=['GET'])
def blog(blog_slug):
    _post=posts.query.filter_by(slug=blog_slug).first()
    return render_template('blog.html' ,post=_post )

@app.route('/addblog',methods = ['GET','POST'])
def addblog():

    if('user' in session and session['user']==username and request.method=='GET'):
        return render_template('addblog.html')
    if(request.method=='POST'):
        title_ = request.form.get('title')
        content_ = request.form.get('content')
        slug_ = request.form.get('slug')

        entry = posts(title=title_,content=content_,slug=slug_)

        db.session.add(entry)
        db.session.commit()
        flash("{} blog added ".format(title_),'success')

        return redirect('/admin')
    else:
        return redirect('/login')

@app.route('/logout',methods = ['GET','POST'])
def logout():
    session.pop('user')
    return redirect('/login')

@app.route('/login',methods = ['GET','POST'])
def login_():
    if  (request.method == 'POST'):
        user_=request.form.get('username')
        pass_=request.form.get('password')

        if(user_==username and pass_==password):
            session['user']=user_
            return redirect('/admin')



    return render_template('login.html')



@app.route('/admin',methods=['GET','POST'])
def admin():
    post_=posts.query.filter_by().all()

    if('user' in session and session['user']==username):
        return render_template('admin.html',_post=post_)


    if(request.method == 'POST'):
        user_=request.form.get('username')
        pass_=request.form.get('password')

        if(user_==username and pass_==password):
            session['user']=user_
            return render_template('admin.html',_post=post_)
        else:
            flash("wrong credentials",'fail')
            return render_template('login.html')


    else:
        return render_template('login.html')

@app.route('/uploader',methods = ['GET','POST'])
def uploader():

    if('user' in session and session['user']==username):
        if(request.method=='POST'):
            f=request.files['file1']
            f.save(os.path.join(app.config['UPLOAD_FOLDER']),secure_filename(f.filename))
            flash("{} uploaded ".format(f.filename),'success')

            return redirect('/admin')

@app.route('/delete_post/<string:ids>',methods=['GET','POST'])
def delete_post(ids):
    if('user' in session and session['user']==username):
        post=posts.query.filter_by(id=ids).first()
        a=post.title
        db.session.delete(post)
        db.session.commit()
        flash("{} deleted ".format(a),'success')
        return redirect('/admin')

    return redirect('/admin')

@app.route('/edit_post/<string:ida>',methods=['GET','POST'])
def edit_post(ida):

     post=posts.query.filter_by(id=ida).first()
     a=post.title
     if('user' in session and session['user']==username):
         if (request.method=='POST'):


             post.title = request.form.get('title')
             post.content = request.form.get('content')
             post.slug = request.form.get('slug')
             db.session.commit()

             flash("{} updated ".format(a),'success')
             return redirect('/admin')
         else:
             return render_template('/edit.html',post=post)
     else:
         return redirect('/login')





@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/bsc')
def bsc():
    return render_template('bsc.html')

@app.route('/msc')
def msc():
    return render_template('msc.html')

@app.route('/mphil')
def mphil():
    return render_template('mphil.html')

@app.route('/phd')
def phd():
    return render_template('phd.html')


app.run(debug=True)
