import google.appengine.ext.ndb as ndb

class Creak(ndb.Model):

    creak = ndb.StringProperty()
    time = ndb.DateTimeProperty(auto_now_add = True)
    user = ndb.StringProperty()
