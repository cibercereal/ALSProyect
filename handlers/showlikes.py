import webapp2
from webapp2_extras import jinja2
from model.register import Register
from model.creak import Creak
from model.follow import Follow
import time
from model.like import Like
import google.appengine.ext.ndb as ndb
from model.notification import Notification

class ShowLikes(webapp2.RequestHandler):
    def get(self):
        try:
            id = self.request.GET["id"]
            user = ndb.Key(urlsafe=id).get()
            noReadMsg = Notification.query(Notification.user == user.username, Notification.read == 0)
            for i in noReadMsg:
                if i.read == 0:
                    noReadMsg = 0
                break

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
                "liked_creaks": var,
                "noReadMsg": noReadMsg
            }
            jinja = jinja2.get_jinja2(app=self.app)
            self.response.write(jinja.render_template("showlikes.html", **values))
            return
        except:
            self.response.write("An error occurred.")
        pass

    def post(self):
        pass

app = webapp2.WSGIApplication([
    ('/showlikes', ShowLikes)
])