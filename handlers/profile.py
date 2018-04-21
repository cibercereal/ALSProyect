import webapp2
from webapp2_extras import jinja2
import google.appengine.ext.ndb as ndb
from model.creak import Creak
from model.register import Register

class Profile(webapp2.RequestHandler):
    def get(self):
        id = self.request.GET["id"]
        user = ndb.Key(urlsafe=id).get()
        if user:
            values = {
                "username": user.username,
                "name": user.name,
                "surname": user.surname,
                "email": user.email,
                "creaks": user.creaks,
                "follow": user.follow,
                "followers": user.followers,
                "id": id
            }

            jinja = jinja2.get_jinja2(app=self.app)
            self.response.write(jinja.render_template("profile.html", **values))
            return

    def post(self):
        pass


app = webapp2.WSGIApplication([
    ('/profile', Profile)
])