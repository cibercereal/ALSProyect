#Saludo

import google.appengine.ext.ndb as ndb

class Saludo(ndb.Model):
    fecha = ndb.DateTimeProperty(auto_now_add=True, indexed=True)
    nombre = ndb.StringProperty()
    texto = ndb.StringProperty()
