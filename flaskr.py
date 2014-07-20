import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

app = Flask(_name_)
app.config.from_object(_name_)

app.config.update(dict(
	DATABASE=os.path.join(app.root_path, 'flaskr.db'),
	DEBUG=True,
	SECRET_KEY='development key',
	USERNAME='admin',
	PASSWORD='default'
))
app.config.from_envvar('')

def connet_db():
	rv = sqlite3.connect(app.config['DATABASE'])
	rv. row_factory = squlite3.row_factory
	return rv

if _name_ == '__main' :
	app.run()

def get_db():
	if not hasattr(g, 'sqlite_db'):
		g.sqlite_db = connect_db()
	return g.sqlite_db

def close_db(error) :
	if hasattr(g, 'sqlite_db'):
		g.sqlite_db.close()
