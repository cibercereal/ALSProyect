import webapp2
from webapp2_extras import jinja2
from model.register import Register
from model.creak import Creak
from model.follow import Follow
import time
from model.like import Like
from model.notification import Notification
import google.appengine.ext.ndb as ndb

class DeleteNotification(webapp2.RequestHandler):
    def get(self):
        try:
            id = self.request.GET["id"]
            user = ndb.Key(urlsafe=id).get()
            try:
                idnot = self.request.GET["idnotification"]
                notification = ndb.Key(urlsafe=idnot).get()
            except:
                notification = None

            if notification:
                notification.key.delete()
                time.sleep(0.5)
                self.redirect("/notification/shownotifications?id=" + id)
        except:
            self.response.write("An error occurred.")
            return

    def post(self):
        pass

app = webapp2.WSGIApplication([
    ('/notification/deletenotification', DeleteNotification)
], debug=True)