from flask import Flask,render_template,request,session,redirect,url_for

app=Flask(__name__)

username_='madan'
password_='55'

app.secret_key='hYfkC4NvaG58r8bfPX71'




@app.route('/',methods=['GET','POST'])
def index():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('pass')

        if username == username_ and password == password:
            session['user'] = username_
            return redirect('/auth')
        else:
            return redirect('/')
    else:
        return render_template('index.html')

@app.route('/logout',methods=['GET','POST'])
def logout():
    session.pop('user')
    return redirect('/')


@app.route('/auth',methods=['GET','POST'])
def auth():
    if request.method == 'GET':
        if 'user' in session and session['user']==username_:
            return render_template('auth.html')
        else:
            return redirect('/')

    else:
        return redirect('/')

app.run(debug=True)