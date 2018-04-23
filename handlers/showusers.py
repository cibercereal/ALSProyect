import webapp2
from webapp2_extras import jinja2
from model.register import Register
from model.creak import Creak
from model.follow import Follow
import time
import google.appengine.ext.ndb as ndb
from model.like import Like
from model.notification import Notification

class ShowUsers(webapp2.RequestHandler):
    def get(self):
        search = self.request.get("search", "").strip()
        id = self.request.GET["id"]
        user = ndb.Key(urlsafe=id).get()
        noReadMsg = Notification.query(Notification.user == user.username, Notification.read == 0)
        if len(search) == 0:
            self.response.write("User to search can not be null.")
            return

        users = Register.query(Register.username == search)

        if users.count() == 0:
            user_creaks = Creak.query(Creak.user == user.username).order(-Creak.time)
            values = {
                "error_login": "The user you are looking for does not exist.",
                "username": user.username,
                "name": user.name,
                "surname": user.surname,
                "creaks": user.creaks,
                "follow": user.follow,
                "followers": user.followers,
                "id": id,
                "user_creaks": user_creaks,
                "noReadMsg": noReadMsg
            }
            jinja = jinja2.get_jinja2(app=self.app)
            self.response.write(jinja.render_template("welcome.html", **values))
            return
        else:
            for i in users:
                users = Register(username=i.username,name=i.name,surname=i.surname,
                                email=i.email,creaks=i.creaks,follow=i.follow,followers=i.followers)

            user_creaks = Creak.query(Creak.user == users.username).order(-Creak.time)

            follow = Follow.query(ndb.AND(Follow.username == user.username, Follow.usernameToFollow == users.username))
            likes = []
            like = Like.query(Like.iduser == user.username)
            for j in like:
                likes.append(j.idcreak)

            if follow.count() != 0:
                values = {
                    "id": id,
                    "username": user.username,
                    "name": user.name,
                    "surname": user.surname,
                    "creaks": user.creaks,
                    "follow": user.follow,
                    "followers": user.followers,
                    "usernameSearch": users.username,
                    "nameSearch": users.name,
                    "surnameSearch": users.surname,
                    "creaksSearch": users.creaks,
                    "followSearch": users.follow,
                    "followersSearch": users.followers,
                    "user_creaks": user_creaks,
                    "followed": "followed",
                    "like": likes,
                    "noReadMsg": noReadMsg
                }
                jinja = jinja2.get_jinja2(app=self.app)
                self.response.write(jinja.render_template("viewuser.html", **values))
                return

            else:
                values = {
                    "id": id,
                    "username": user.username,
                    "name": user.name,
                    "surname": user.surname,
                    "creaks": user.creaks,
                    "follow": user.follow,
                    "followers": user.followers,
                    "usernameSearch": users.username,
                    "nameSearch": users.name,
                    "surnameSearch": users.surname,
                    "creaksSearch": users.creaks,
                    "followSearch": users.follow,
                    "followersSearch": users.followers,
                    "user_creaks": user_creaks,
                    "noReadMsg": noReadMsg
                }
                jinja = jinja2.get_jinja2(app=self.app)
                self.response.write(jinja.render_template("viewuser.html", **values))
                return

    def post(self):
        id = self.request.GET["id"]
        user = ndb.Key(urlsafe=id).get()

        if user:
            noReadMsg = Notification.query(Notification.user == user.username, Notification.read == 0)
            for i in noReadMsg:
                if i.read == 0:
                    noReadMsg = 0
                break
            try:
                edit = self.request.GET["edit"]

                values = {
                    "username": user.username,
                    "name": user.name,
                    "surname": user.surname,
                    "email": user.email,
                    "id": id,
                    "noReadMsg": noReadMsg
                }
                jinja = jinja2.get_jinja2(app=self.app)
                self.response.write(jinja.render_template("edituser.html", **values))
                return
            except:
                name = self.request.get("name", "").strip()
                surname = self.request.get("surname", "").strip()
                email = self.request.get("email", "").strip()

                if len(name) == 0 or len(surname) == 0 or len(email) == 0:
                    self.response.write("It is necessary to complete all fields.")

                user.name = name
                user.surname = surname
                user.email = email
                user.put()
                self.redirect("/welcome?id="+id)
                return
app = webapp2.WSGIApplication([
    ('/showusers', ShowUsers)
], debug=True)