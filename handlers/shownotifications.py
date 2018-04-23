import webapp2
from webapp2_extras import jinja2
from model.register import Register
from model.creak import Creak
from model.follow import Follow
import time
from model.like import Like
from model.notification import Notification
import google.appengine.ext.ndb as ndb

class ShowNotifications(webapp2.RequestHandler):
    def get(self):
        try:
            id = self.request.GET["id"]
            user = ndb.Key(urlsafe=id).get()

            noReadMsg = Notification.query(Notification.user == user.username, Notification.read == 0)
            for i in noReadMsg:
                i.read = 1
                i.put()
                time.sleep(0.5)

            notifications = Notification.query(Notification.user == user.username).order(-Notification.date)

            values = {
                "username": user.username,
                "name": user.name,
                "surname": user.surname,
                "notifications": notifications,
                "id": id
            }
            jinja = jinja2.get_jinja2(app=self.app)
            self.response.write(jinja.render_template("shownotifications.html", **values))
            return
        except:
            self.response.write("An error occurred.")
            return

    def post(self):
        pass

app = webapp2.WSGIApplication([
    ('/shownotifications', ShowNotifications)
], debug=True)