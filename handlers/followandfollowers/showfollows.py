import webapp2
import google.appengine.ext.ndb as ndb
from model.follow import Follow
import time
from model.creak import Creak
from model.register import Register
from model.notification import Notification
from webapp2_extras import jinja2

class ShowFollows(webapp2.RequestHandler):
    def get(self):
        try:
            id = self.request.GET["id"]
            user = ndb.Key(urlsafe=id).get()
            noReadMsg = Notification.query(Notification.user == user.username, Notification.read == 0)
            for i in noReadMsg:
                if i.read == 0:
                    noReadMsg = 0
                break

            follow = Follow.query(Follow.username == user.username)
            values = {
                "username": user.username,
                "name": user.name,
                "surname": user.surname,
                "creaks": user.creaks,
                "follow": user.follow,
                "followers": user.followers,
                "id": id,
                "follows": follow,
                "noReadMsg": noReadMsg
            }
            jinja = jinja2.get_jinja2(app=self.app)
            self.response.write(jinja.render_template("showfollow.html", **values))
            return
        except:
            self.response.write("An error occurred.")
            return

    def post(self):
        pass

app = webapp2.WSGIApplication([
    ('/followandfollowers/showfollows', ShowFollows)
])