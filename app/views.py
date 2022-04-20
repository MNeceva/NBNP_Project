from app import app #from package app import the variable app created in __init__.py
from app.forms import *
from flask import render_template, session, request, redirect, jsonify, make_response, url_for
from flask_login import current_user

@app.route('/')
def index():
    if not current_user.is_authenticated:
        return render_template('index.html')
    else: 
        return redirect(url_for('main.upload_files'))
        