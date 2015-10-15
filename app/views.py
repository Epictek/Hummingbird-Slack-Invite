from flask import render_template, request, redirect, url_for, session, flash
from app import app, models, db
import uuid
import re
import requests
from sqlalchemy import *
import os

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        invite_id = str(uuid.uuid4())
        email = request.form['email']
        hb_user = request.form['hbuser']
        print(email)
        print(hb_user)
        if not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):
            flash("Please enter a valid email address")
            return redirect(url_for('index'))
        r = requests.get("https://hummingbird.me/api/v1/users/" + hb_user)
        if r.status_code == 404:
            flash("User not found")
            return redirect(url_for('index'))
        if r.status_code != 200:
            flash("Hummingbird is up in flames? Try later.")
            return redirect(url_for('index'))
        user = models.User.query.filter(or_(models.User.hb_user==hb_user, models.User.email==email)).first()
        print(user)
        if user != None:
            if user.verified == True:
                flash("Account already verified. Another invite has been sent.")
                data = {
                    'email': user.email,
                    'token': os.environ['slack-token'],
                    'set_active': 'true',
                    'first_name': hb_user,
                }
                r = requests.post(
                    'http://superhbchat.slack.com/api/users.admin.invite',
                    params=data
                ).json()
                return redirect(url_for('index'))
        user = models.User.query.filter(and_(models.User.hb_user==hb_user, models.User.email==email)).first()
        if user != None:
            session['invite_id'] = user.invite_id
            return redirect(url_for('verify'))
        user = models.User(invite_id, hb_user, email, request.remote_addr)
        db.session.add(user)
        db.session.commit()
        session['invite_id'] = invite_id
        return redirect(url_for('verify'))
    return render_template('index.html')


@app.route('/verify', methods=['GET', 'POST'])
def verify():
    invite_id = session['invite_id']
    return render_template('verify.html', invite_id=invite_id)
