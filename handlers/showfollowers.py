import webapp2
import google.appengine.ext.ndb as ndb
from model.follow import Follow
import time
from model.creak import Creak
from model.register import Register
from webapp2_extras import jinja2

class ShowFollowers(webapp2.RequestHandler):
    def get(self):
        id = self.request.GET["id"]
        user = ndb.Key(urlsafe=id).get()

        follow = Follow.query(Follow.usernameToFollow == user.username)
        values = {
            "username": user.username,
            "name": user.name,
            "surname": user.surname,
            "creaks": user.creaks,
            "follow": user.follow,
            "followers": user.followers,
            "id": id,
            "follows": follow
        }
        jinja = jinja2.get_jinja2(app=self.app)
        self.response.write(jinja.render_template("showfollowers.html", **values))
        return

    def post(self):
        pass

app = webapp2.WSGIApplication([
    ('/showfollowers', ShowFollowers)
])