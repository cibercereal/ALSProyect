import webapp2
import google.appengine.ext.ndb as ndb
import time
from model.creak import Creak
from model.register import Register
from webapp2_extras import jinja2

class AddCreakHandler(webapp2.RequestHandler):
    def get(self):
        pass

    def post(self):
        id = self.request.GET["id"]
        user = ndb.Key(urlsafe=id).get()
        u = Register.query(Register.username == user.username)
        if user:
            creak = self.request.get("realCrunch", "").strip()

            if len(creak) != 0:
                cr = Creak(creak=creak,user=user.username,name=user.name,surname=user.surname)
                cr.put()
                time.sleep(1)
                #modificar el numero de creaks escritos
                user.creaks = user.creaks + 1
                user.put()
                user_id = u.fetch(1)[0].key.urlsafe()
                self.redirect("/welcome?id=" + user_id)
            else:
                self.response.write("Creak can not be null.")
                return
        else:
            self.response.write("You must be loggin to send a creak.")
            return

app = webapp2.WSGIApplication([
    ('/addcreak', AddCreakHandler)
])