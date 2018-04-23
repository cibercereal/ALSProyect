import webapp2
from webapp2_extras import jinja2
from model.register import Register
from model.creak import Creak
from model.follow import Follow
import time
from model.like import Like
from model.notification import Notification
import google.appengine.ext.ndb as ndb

class LikeCreak(webapp2.RequestHandler):
    def get(self):
        try:
            id = self.request.GET["id"]
            user = ndb.Key(urlsafe=id).get()
    
            try:
                idcreak = self.request.GET["idcreak"]
                creak = ndb.Key(urlsafe=idcreak).get()
            except:
                creak = None
    
            if creak:
                like = Like(idcreak=creak.key.urlsafe(), iduser=user.username)
                like.put()
                time.sleep(1)
                if user.username != creak.user:
                    notification = Notification(user=creak.user,msg="@"+user.username+" liked your creak: '"+creak.creak+"'",read=0)
                    notification.put()
                    time.sleep(1)
                self.redirect("/welcome?id="+id)
            else:
                self.response.write("An error occurred.")
        except:
            self.response.write("An error occurred.")
            return

    def post(self):
        pass

app = webapp2.WSGIApplication([
    ('/likecreak', LikeCreak)
], debug=True)