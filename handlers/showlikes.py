import webapp2
from webapp2_extras import jinja2
from model.register import Register
from model.creak import Creak
from model.follow import Follow
import time
from model.like import Like
import google.appengine.ext.ndb as ndb

class ShowLikes(webapp2.RequestHandler):
    def get(self):
        try:
            id = self.request.GET["id"]
            user = ndb.Key(urlsafe=id).get()

            likes = Like.query(Like.iduser == user.username)
            var = []
            for i in likes:
                var.append(ndb.Key(urlsafe=i.idcreak).get())
                print(var)
            #liked_creaks = Creak.query(Creak.key.urlsafe().IN(var)).order(-Creak.time)
            values = {
                "username": user.username,
                "name": user.name,
                "surname": user.surname,
                "creaks": user.creaks,
                "follow": user.follow,
                "followers": user.followers,
                "id": id,
                "liked_creaks": var
            }
            jinja = jinja2.get_jinja2(app=self.app)
            self.response.write(jinja.render_template("showlikes.html", **values))
            return
        except:
            self.response.write("An error occurred")
        pass

    def post(self):
        pass

app = webapp2.WSGIApplication([
    ('/showlikes', ShowLikes)
])