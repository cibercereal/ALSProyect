import google.appengine.ext.ndb as ndb

class Creak(ndb.Model):

    creak = ndb.TextProperty()
    time = ndb.DateTimeProperty(auto_now_add = True)
    user = ndb.StringProperty()
    name = ndb.StringProperty()
    surname = ndb.StringProperty()
