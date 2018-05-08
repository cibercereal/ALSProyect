import webapp2
import google.appengine.ext.ndb as ndb
from model.follow import Follow
import time
from model.creak import Creak
from model.like import Like
from model.user import User
from model.register import Register
from webapp2_extras import jinja2
import unicodedata

class DeleteCreak(webapp2.RequestHandler):
    def get(self):
        try:
            id = self.request.GET["id"]
            user = ndb.Key(urlsafe=id).get()
            try:
                creak = self.request.get("idcreak", "").strip()
                creak = ndb.Key(urlsafe=creak).get()
            except:
                creak = None
            if creak:
                v = creak.key.urlsafe()
                likes = Like.query()
                for i in likes:
                    if i.idcreak == v:
                        i.key.delete()
                        time.sleep(0.5)

                user.creaks = user.creaks - 1
                user.put()

                creak.key.delete()
                time.sleep(0.5)
                self.redirect("/creak/showcreak?id="+id)
            else:
                self.response.write("An error ocurred.")
                return
        except:
            self.response.write("An error occurred.")
            return

    def post(self):
        pass

app = webapp2.WSGIApplication([
    ('/creak/deletecreak', DeleteCreak)
])