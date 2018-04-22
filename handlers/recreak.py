import webapp2
import google.appengine.ext.ndb as ndb
from model.follow import Follow
import time
from model.creak import Creak
from model.register import Register
from webapp2_extras import jinja2

class Recreak(webapp2.RequestHandler):
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
                p = "RC from "+creak.name+" "+creak.surname+" @"+creak.user+" ==> \r\n  "
                user.creaks = user.creaks + 1
                user.put()

                cr = Creak(creak=p+creak.creak, user=user.username, name=user.name, surname=user.surname)
                cr.put()
                self.redirect("/welcome?id="+id)
            else:
                self.response.write("An error occurred.")
                return
        except:
            self.response.write("An id error occurred.")
            return

    def post(self):
        pass

app = webapp2.WSGIApplication([
    ('/recreak', Recreak)
])