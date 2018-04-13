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
import time
from webapp2_extras import jinja2

import datetime as dt
from model.register import Saludo
from model.register import Register

class MainHandler(webapp2.RequestHandler):
    def get(self):
        jinja = jinja2.get_jinja2(app = self.app)
        saludos = Saludo.query().order(-Saludo.fecha)

        values = {
            "fecha": dt.datetime.today(),
            "saludos": saludos
        }

        self.response.write(jinja.render_template("index.html", **values))

    def post(self):
        name = self.request.get("name","").strip()
        saludo = self.request.get("saludo", "").strip()

        if len(name) == 0 or len(saludo) == 0:
            self.response.write("Se requiere un nombre y un saludo.")
            return

        saludo = Saludo(nombre=name, texto=saludo)
        saludo.put()
        time.sleep(1)
        self.redirect("/")

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)

