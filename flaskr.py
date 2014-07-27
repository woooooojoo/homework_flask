
import os
import re
import json
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash


app = Flask(__name__)
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'flaskr.db'),
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))

app.config.from_envvar('FLASKR_SETTINGS', silent=True)


def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()



def get_db():

	if not hasattr(g, 'sqlite_db'):
		g.sqlite_db = connect_db()
	return g.sqlite_db


@app.teardown_appcontext
def close_db(error):

    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.route('/')
def show_entries():
    db = get_db()
    cur = db.execute('select title, text from entries order by id desc')
    entries = cur.fetchall()
    return render_template('show_entries.html', entries=entries)


@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    db.execute('insert into entries (title, text) values (?, ?)',
               [request.form['title'], request.form['text']])
    db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':

        f = open('users.text',"r")
        data=f.read()
        users=json.loads(data)
        f.close()
        for i in users:
   
            if i['email'] == request.form['email'] and i['password']==request.form['password'] :
                
                if i['admin'] == True:
                    session['admin']=True
                    session['logged_in'] = True
                    session['email'] = request.form['email']
                    flash('You were logged in')
                    return redirect(url_for('show_entries'))
                else :
                    session['admin']=False
                    session['logged_in'] = True
                    session['email'] = request.form['email']
                    flash('You were logged in')
                    return redirect(url_for('show_entries'))


            else:
                error="email or password is wrong please re-write."
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))



@app.route('/signup', methods=['GET','POST'])
def signup():
    message = None
    if request.method == "POST" :
        if request.form['email'] =="":
            message = "Email is empty" 
        elif request.form['password']=="":
            message = "Password is empty"
        elif request.form['password_check']=="":
            message = "Password is empty"
        elif bool(re.search("\w+(\@)\w+(.com|.ac.kr|.net)", request.form['email']))==False:
            message ="retry to write email "
        elif request.form['password']!="":
            if len(request.form['password']) < 8 or len(request.form['password']) >20 :
                message="retry to write password"
            elif bool(re.search("[a-z]+",request.form['password'])) == False:
                message="retry to write password"
            elif bool(re.search("[A-Z]+",request.form['password'])) == False:
                message="retry to write password"
            elif bool(re.search("[0-9]+",request.form['password'])) == False:
                message="retry to write password"
            elif bool(re.search("\W+",request.form['password'])) == False:
                message="retry to write password"
            elif request.form['password'] != request.form['password_check'] :
                message="retry to write password check"
            else :
                if os.path.exists("users.text") == True:
                   
                    users=[]
                    test_repeat=[]
                    f=open("users.text","r")
                    data=f.read()
                    open_users=json.loads(data)


                    answers_admin = 'admin' in request.form
                    for user_dic in open_users:
                        users.append(user_dic)

                    for user in open_users:
                        x = user['email']
                        test_repeat.append(x)
                    f.close()


                    if request.form['email'] in test_repeat:
                        message= "This email is already used."
                    else:
                        # if 'admin' in request.form: line145
                        #     answers_admin = True
                        # else :
                        #     answers_admin = False  
                        message= "Sign up successful "

                        info={}
                        info['email']=request.form['email']
                        info['password']=request.form['password']
                        info['admin']= answers_admin


                        users.append(info) 
                        f=open("users.text","w")
                        f.write(json.dumps(users))
                        f.close()

                else:   
                    if 'admin' in request.form:
                        answers_admin = True
                    else :
                        answers_admin = False              
                    message= "Sign up successful"
                    users=[]
                    info={}
                    info['email']=request.form['email']
                    info['password']=request.form['password']
                    info['admin']=answers_admin

                    users.append(info) 
                    f=open("users.text","w")
                    f.write(json.dumps(users))
                    f.close()


    return render_template('signup.html', message = message)  

@app.route('/userslist', methods=['GET','POST'])
def userslist():
    if session['admin'] == True:
        userslist=None
        f=open('users.text','r')
        data=f.read()
        userslist=json.loads(data)
        return render_template('userslist.html',userslist=userslist)
    else:
        return redirect(url_for('show_entries'))

@app.route('/email_check',methods=['GET','POST'])
def email_check():
    f=open('users.text','r')
    data=f.read()
    userslist=json.loads(data)
    result={}
    for user in userslist:
        email=user['email']
        if email == request.form['email']:
            result['message'] = "this email is already existed."
            return json.dumps(result)
    result['message']="Okay"
    return json.dumps(result)
    #result['message']="Okay" 
    #for user in userslist:
    #     email=user[email]
    #     if email == request.form['email']:
    #         result['message'] = "this email is already existed."
    # return json.dumps(result)
 






if __name__ == '__main__':
	app.run()
