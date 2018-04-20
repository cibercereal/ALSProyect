
import google.appengine.ext.ndb as ndb

class User(ndb.Model):

    username = ndb.StringProperty()
    name = ndb.StringProperty()
    surname = ndb.StringProperty()
    email = ndb.StringProperty()
    birthday = ndb.StringProperty()
    creaks = ndb.IntegerProperty()
    follow = ndb.IntegerProperty()
    followers = ndb.IntegerProperty()





