import requests
from app import app, db, models
import os

r = requests.get("https://hummingbird.me/stories?page=1&user_id=Slack") 
r = r.json() 

for story in r['stories']: 
    if story['type'] == "comment": 
        hb_user = story['poster_id']
        invite_id = story['comment']
        print(invite_id)
        print(hb_user)
        users = models.User.query.filter_by(hb_user=hb_user).all()
        for user in users:
            if user.invite_id in story['comment']:
                print(user)
                if user != None:
                    if user.verified == False:
                        print(user.email)
                        data = {
                            'email': user.email,
                            'token': os.environ['SLACKTOKEN'],
                            'set_active': 'true',
                            'first_name': hb_user,
                        }
                        r = requests.post(
                             'http://humchat.slack.com/api/users.admin.invite',
                            params=data
                        ).json()
                        if r['ok'] == True:
                            user.verified = True
                            db.session.commit()
