import google.appengine.ext.ndb as ndb

class Notification(ndb.Model):

    user = ndb.StringProperty()
    date = ndb.DateProperty(auto_now_add = True)
    msg = ndb.TextProperty()
    read = ndb.IntegerProperty()