import webapp2
from webapp2_extras import jinja2
from model.user import User
import google.appengine.ext.ndb as ndb
from model.creak import Creak
from model.follow import Follow
from model.register import Register
from model.like import Like
from model.notification import Notification

class Welcome(webapp2.RequestHandler):
    def get(self):
        id = self.request.GET["id"]
        user = ndb.Key(urlsafe=id).get()
        follows = Follow.query(Follow.username == user.username)
        noReadMsg = Notification.query(Notification.user == user.username, Notification.read == 0)
        for i in noReadMsg:
            if i.read == 0:
                noReadMsg = 0
            break
        creaks = []
        if follows.count() != 0:
            for i in follows:
                if i.username == user.username:
                    creaks.append(i.usernameToFollow)

            user_creaks = Creak.query(ndb.OR(Creak.user == user.username, Creak.user.IN(creaks))).order(-Creak.time)
            likes = []
            like = Like.query(Like.iduser == user.username)
            for j in like:
                likes.append(j.idcreak)

            values = {
                "username": user.username,
                "name": user.name,
                "surname": user.surname,
                "creaks": user.creaks,
                "follow": user.follow,
                "followers": user.followers,
                "id": id,
                "user_creaks": user_creaks,
                "like": likes,
                "noReadMsg": noReadMsg
            }
        else:
            user_creaks = Creak.query(Creak.user == user.username).order(-Creak.time)
            likes = []
            like = Like.query(Like.iduser == user.username)
            for j in like:
                likes.append(j.idcreak)

            values = {
                "username": user.username,
                "name": user.name,
                "surname": user.surname,
                "creaks": user.creaks,
                "follow": user.follow,
                "followers": user.followers,
                "id": id,
                "user_creaks": user_creaks,
                "like": likes,
                "noReadMsg": noReadMsg
            }
        jinja = jinja2.get_jinja2(app=self.app)
        self.response.write(jinja.render_template("welcome.html", **values))
        return
    def post(self):
        pass


app = webapp2.WSGIApplication([
    ('/welcome', Welcome)
], debug=True)