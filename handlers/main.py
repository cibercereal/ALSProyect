#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
from webapp2_extras import jinja2
from model.register import Register

from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import webapp
from google.appengine.api import users

import time
from google.appengine.api import users


class MainHandler(webapp2.RequestHandler):
    def get(self):

        values = {

        }

        jinja = jinja2.get_jinja2(app=self.app)
        self.response.write(jinja.render_template("index.html", **values))

    def post(self):
        username = self.request.get("username", "").strip()
        password = self.request.get("passwd", "").strip()

        if len(username) == 0 or len(password) == 0:
            self.response.write("It is necessary to complete all fields.")
            return

        if len(username) < 5:
            self.response.write("Username must have at least 5 characters.")

        user = Register.query(Register.username == username, Register.password == password)

        if user.count() == 1:
            user_id = user.fetch(1)[0].key.urlsafe()
            self.redirect("/welcome?id="+user_id)
            return
        else:
            values = {
                "error_login": "Incorrect username or password"
            }

            jinja = jinja2.get_jinja2(app=self.app)
            self.response.write(jinja.render_template("index.html", **values))
            return

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)

