import webapp2
import os
import random
import time
import google.appengine.ext.ndb as ndb
from webapp2_extras import jinja2
from model.register import Register

class RegisterHandler(webapp2.RequestHandler):
    def get(self):
        jinja = jinja2.get_jinja2(app=self.app)
        users = Register.query()

        values = {
            "users": users
        }

        self.response.write(jinja.render_template("register.html", **values))

    def post(self):
        name = self.request.get("name", "").strip()
        surname = self.request.get("surname", "").strip()
        username = self.request.get("username", "").strip()
        email = self.request.get("email", "").strip()
        birthdate = self.request.get("birthdate", "").strip()
        password = self.request.get("passwd", "").strip()
        rpassword = self.request.get("rpasswd", "").strip()
        creaks = 0
        follow = 0
        followers = 0

        if len(name) == 0 or len(surname) == 0 or len(username) == 0 or \
                len(email) == 0 or len(birthdate) == 0 or len(password) == 0\
                or len(rpassword) == 0:
            self.response.write("It is necessary to complete all fields of the record.")
            return

        if len(username) < 5:
            self.response.write("Username must have at least 5 characters.")

        if rpassword != password:
            self.response.write("Passwords do not match.")
            return

        user = Register(username=username, name=name, surname=surname,
                        email=email, birthdate=birthdate, password=password, creaks=creaks, follow=follow, followers=followers)
        userToPut = Register.query(ndb.OR(Register.username == username, Register.email == email))

        if userToPut.count() > 0:
            values = {
                "error_register": "The username or email already exists."
            }

            jinja = jinja2.get_jinja2(app=self.app)
            self.response.write(jinja.render_template("register.html", **values))
            return
        else:
            user.put()
            time.sleep(1)
            self.redirect("/")

app = webapp2.WSGIApplication([
    ('/register', RegisterHandler)
], debug=True)