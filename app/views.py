from flask import render_template, request, redirect, url_for, session, flash
from app import app, models, db
import uuid
import re
import requests
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        invite_id = str(uuid.uuid4())
        email = request.form['email']
        hbuser = request.form['hbuser']
        if not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):
            flash("Please enter a valid email address")
            return redirect(url_for('index'))
        r = requests.get("https://hummingbird.me/api/v1/users/" + hbuser)
        if r.status_code == 404:
            flash("User not found")
            return redirect(url_for('index'))
        if r.status_code != 200:
            flash("Hummingbird is up in flames? Try later.")
            return redirect(url_for('index'))
        invite = models.Invite(invite_id, email, request.form['hbuser'], request.remote_addr)
        db.session.add(invite)
        db.session.commit()
        session['invite_id'] = invite_id
        return redirect(url_for('verify'))
    return render_template('index.html')


@app.route('/verify', methods=['GET', 'POST'])
def verify():
    invite_id = session['invite_id']
    return render_template('verify.html', invite_id=invite_id)
