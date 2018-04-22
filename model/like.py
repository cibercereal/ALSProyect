import google.appengine.ext.ndb as ndb

class Like(ndb.Model):

    idcreak = ndb.TextProperty()
    iduser = ndb.StringProperty()