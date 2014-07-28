from flask import Flask, request, session, g, redirect, abort, url_for, render_template, flash
import pusher
app = Flask(__name__)
app.config['DEBUG'] = True

# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.

p = pusher.Pusher(
	app_id='83073',
	key='e51a7de31250e2d1b3bd',
	secret='488bbeeeb79dde9eacc7'
)
app.secret_key='hihihihi'

@app.route('/')
def index():
	if 'username' in session:
		return render_template('index.html')
	else:
		return redirect(url_for('login'))

@app.route('/login',methods=['GET','POST'])
def login():
	if request.method =='POST':
		session['username']=request.form['username']
		p['likelion'].trigger('notification',{"username":session['username']})
		return redirect(url_for('index'))
	else:
		return render_template('login.html')

@app.route('/chat',methods=['GET','POST'])
def chat():
	if request.method == 'POST':
		message = request.form['message']
		p['likelion'].trigger('chatting',{"message":message, "username":session['username']})
		return render_template('index.html')

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404





