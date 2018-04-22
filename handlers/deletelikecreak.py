import webapp2
from webapp2_extras import jinja2
from model.register import Register
from model.creak import Creak
from model.follow import Follow
import time
from model.like import Like
import google.appengine.ext.ndb as ndb

class DeleteLikeCreak(webapp2.RequestHandler):
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
                like = Like.query(Like.iduser == user.username)
                for i in like:
                    if i.idcreak == idcreak:
                        li = i
                li.key.delete()
                time.sleep(0.5)
                self.redirect("/welcome?id=" + id)
            else:
                self.response.write("An error occurred.")
        except:
            self.response.write("An error occurred.")
            return

    def post(self):
        pass

app = webapp2.WSGIApplication([
    ('/deletelikecreak', DeleteLikeCreak)
], debug=True)