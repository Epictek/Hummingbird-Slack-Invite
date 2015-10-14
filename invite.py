import requests
from app import app, db, models

r = requests.get("https://hummingbird.me/stories?page=1&user_id=Slack") 
r = r.json() 

for story in r['stories']: 
    if story['type'] == "comment": 
        hb_user = story['poster_id']
        invite_id = story['comment'].strip()
        print(invite_id)
        print(hb_user)
        user = models.User.query.filter_by(hb_user=hb_user, invite_id=invite_id).first()
        print(user)
        if user != None:
            if user.invite_sent == False:
                user.invite_sent = True
                print(user.email)
                data = {
                    'email': user.email,
                    'token': "",
                    'set_active': 'true',
                    'first_name': hb_user,
                }
                r = requests.post(
                    'http://superhbchat.slack.com/api/users.admin.invite',
                    params=data
                ).json()
                print(r)
                db.session.commit()