#Saludo

import google.appengine.ext.ndb as ndb

class Saludo(ndb.Model):
    fecha = ndb.DateTimeProperty(auto_now_add=True, indexed=True)
    nombre = ndb.StringProperty()
    texto = ndb.StringProperty()

class Register(ndb.Model):
    username = ndb.StringProperty()
    name = ndb.StringProperty()
    surname = ndb.StringProperty()
    email = ndb.StringProperty()
    birthdate = ndb.DateProperty()
    password = ndb.StringProperty()

class Login(ndb.Model):
    username = ndb.StringProperty()
    password = ndb.StringProperty()