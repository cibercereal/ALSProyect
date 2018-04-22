import webapp2
import google.appengine.ext.ndb as ndb
from model.follow import Follow
import time
from model.creak import Creak
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
                user.creaks = user.creaks - 1
                user.put()

                creak.key.delete()
                time.sleep(0.5)
                self.redirect("/showcreak?id="+id)
            else:
                self.response.write("An error ocurred.")
                return
        except:
            self.response.write("An error occurred.")
            return

    def post(self):
        pass

app = webapp2.WSGIApplication([
    ('/deletecreak', DeleteCreak)
])