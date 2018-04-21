import google.appengine.ext.ndb as ndb

class Follow(ndb.Model):

    username = ndb.StringProperty()
    usernameToFollow = ndb.StringProperty()
