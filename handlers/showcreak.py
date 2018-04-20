import webapp2
from webapp2_extras import jinja2
import google.appengine.ext.ndb as ndb
from model.creak import Creak
from model.register import Register

class ShowCreakHandler(webapp2.RequestHandler):
    def get(self):
        id = self.request.GET["id"]
        user = ndb.Key(urlsafe=id).get()
        if user:
            user_creaks = Creak.query(Creak.user == user.username).order(-Creak.time)
            values = {
                "username": user.username,
                "name": user.name,
                "surname": user.surname,
                "creaks": user.creaks,
                "follow": user.follow,
                "followers": user.followers,
                "id": id,
                "user_creaks": user_creaks
            }
            jinja = jinja2.get_jinja2(app=self.app)
            self.response.write(jinja.render_template("showcreak.html", **values))
            return

    def post(self):
        pass

app = webapp2.WSGIApplication([
    ('/showcreak', ShowCreakHandler)
])