import cgi
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

import webapp2

def session_key(session_name):
    """Constructs a Datastore key for a Guestbook entity with guestbook_name."""
    return ndb.Key('Session', session_name)

class Session(ndb.Model):
    """Description, start and end time and date and location for a session"""

    name = ndb.StringProperty()
    description = ndb.StringProperty()
    start_date = ndb.DateTimeProperty(auto_now_add=False)
    end_date = ndb.DateTimeProperty(auto_now_add=False)
    location = ndb.StringProperty()
    speakers = ndb.StringProperty()
    biography = ndb.StringProperty()
    survey = ndb.StringProperty()


