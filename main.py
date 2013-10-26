#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
from session import *
import datetime
import time
from time import mktime


MAIN_PAGE_FOOTER_TEMPLATE = """\
    <form action="/" method="post">
      Session Location
      <div><textarea name="session_location" rows="3" cols="60"></textarea></div>
      Session Description
      <div><textarea name="session_description" rows="3" cols="60"></textarea></div>
      Session Speaker(s)
      <div><textarea name="speakers" rows="1" cols="60"></textarea></div>
      Biography
      <div><textarea name="biography" rows="3" cols="60"></textarea></div>
      Session Name
      <div><textarea name="session_name" rows="1" cols="60"></textarea></div>
      Date: <input type="date" name="date">
      Start time: <input type="time" name="start_time">
      End time: <input type="time" name="end_time">
      <div><input type="submit" value="Submit Information"></div>
    </form>

    

   

  </body>
</html>
"""

class MainHandler(webapp2.RequestHandler):

    def get(self):
        self.response.write(MAIN_PAGE_FOOTER_TEMPLATE)
        
    def post(self):
        session_name = self.request.get("session_name")
        date = self.request.get("date")
        start = date + " " + self.request.get("start_time")
        start_timedate = time.strptime(start, "%Y-%m-%d %H:%M")
        end = date + " " + self.request.get("end_time")
        end_timedate = time.strptime(end, "%Y-%m-%d %H:%M")
        session1 = Session(name=session_name,
                           description=self.request.get("session_description"),
                           location=self.request.get("session_location"),
                           parent=ndb.Key('Type', 'Session', 'Name', session_name),
                           start_date=datetime.datetime.fromtimestamp(mktime(start_timedate)),
                           end_date=datetime.datetime.fromtimestamp(mktime(end_timedate)),
                           speakers=self.request.get("speakers"),
                           biography=self.request.get("biography"))
        session1.put()
        self.response.write('stored!')

class DataHandler(webapp2.RequestHandler):

    def get(self):
        session_query = Session.query(ancestor=ndb.Key('Type', 'Session'))
        session = session_query.fetch(100)
        
        self.response.write('Current sessions: ' +  '<br/>')

        for s in session:
            print s.end_date
            self.response.write('Name: ' + noNone(s.name) + '<br/>' +
                                'Decription: ' + noNone(s.description) + '<br/>' +
                                'Location: ' + noNone(s.location) + '<br/>' +
                                'Start Time: ' + noNoneDate(s.start_date) + '<br/>'
                                'End Time: ' + noNoneDate(s.end_date) + '<br/> <br/>')
 
def noNone(input):
    if input is None:
        return 'N/A'
    else:
        return input

def noNoneDate(date):
    if date is None:
        return 'N/A'
    else:
        return date.isoformat()

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/data', DataHandler)
], debug=True)


