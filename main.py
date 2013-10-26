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
      End time: <input type="time" name="start_time">
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
        session1 = Session(name=session_name,
                           description=self.request.get("session_description"),
                           location=self.request.get("session_location"),
                           parent=ndb.Key('Type', 'Session', 'Name', session_name))
        session1.put()
        self.response.write('stored!')

class DataHandler(webapp2.RequestHandler):

    def get(self):
        session_query = Session.query(ancestor=ndb.Key('Type', 'Session'))
        session = session_query.fetch(100)
        
        self.response.write('Current sessions: ' +  '<br/>')

        for s in session:
            self.response.write('Name: ' + s.name + '<br/>' +
                                'Decription: ' + s.description + '<br/>' +
                                'Location: ' + s.location + '<br/>' +
                                'Start Time: ' + s.start_time + '<br/>' +
                                'End Time: ' + s.end_time + '<br/>')

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/data', DataHandler)
], debug=True)


