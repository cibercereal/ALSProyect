import webapp2
import google.appengine.ext.ndb as ndb
from model.follow import Follow
import time
from model.creak import Creak
from model.register import Register
from webapp2_extras import jinja2

class FollowUser(webapp2.RequestHandler):
    def get(self):
        try:
            id = self.request.GET["id"]
            currentuser = ndb.Key(urlsafe=id).get()
            user = self.request.get("user", "").strip()

            user = Register.query(Register.username == user)

            if currentuser and user.count() != 0:
                for i in user:
                    user = i

                unfollow = Follow.query(ndb.AND(Follow.username==currentuser.username, Follow.usernameToFollow==user.username))

                if unfollow.count() == 0:
                    currentuser.follow = currentuser.follow + 1
                    currentuser.put()
                    user.followers = user.followers + 1
                    user.put()

                    follow = Follow(username=currentuser.username, usernameToFollow=user.username)
                    follow.put()
                    time.sleep(1)

                    self.redirect("/user/showusers?search="+user.username+"&id="+id)
                else:
                    currentuser.follow = currentuser.follow -1
                    currentuser.put()
                    user.followers = user.followers - 1
                    user.put()

                    for i in unfollow:
                        unfollow = i

                    unfollow.key.delete()
                    self.redirect("/user/showusers?search=" + user.username + "&id=" + id)
            else:
                self.response.write("An error occurred.")
                return
        except:
            self.response.write("An error occurred.")
            return

    def post(self):
        pass

app = webapp2.WSGIApplication([
    ('/followandfollowers/followuser', FollowUser)
])
