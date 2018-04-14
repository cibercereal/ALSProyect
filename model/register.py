#Saludo

import google.appengine.ext.ndb as ndb

class Register(ndb.Model):
    username = ndb.StringProperty()
    name = ndb.StringProperty()
    surname = ndb.StringProperty()
    email = ndb.StringProperty()
    birthdate = ndb.StringProperty()
    password = ndb.StringProperty()
