import requests
from app import app, db, models
import os
from sqlalchemy import func

r = requests.get("https://hummingbird.me/api/v1/users/Slack/feed") 
r = r.json() 

print(r)

for story in r:
    if story['story_type'] == "comment": 
        hb_user = story['poster']['name']
        invite_id = story['substories'][0]['comment']
        print(invite_id)
        print(hb_user)
#        users = models.User.query.filter_by(hb_user=hb_user).all()
        users = models.User.query.filter(func.lower(models.User.hb_user) == func.lower(hb_user)).all()
        for user in users:
            print(user.hb_user)
            if user.invite_id in invite_id:
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
                        print(r)
                        if r['ok'] == True:
                            user.verified = True
                            db.session.commit()
