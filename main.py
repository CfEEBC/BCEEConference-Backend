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
import json
import jinja2
import os

JINJA_ENVIRONMENT = jinja2.Environment(
        loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
        extensions=['jinja2.ext.autoescape'],
        autoescape=True)

def delete_form_create(session_name):
        delete_form = """<form action="/delete" method="post">
        <input type="hidden" name="key" value="%s">
        <input type="submit" value="Delete"></form>""" % session_name
        return delete_form

class MainHandler(webapp2.RequestHandler):

    def get(self):
        template_values = {}

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))
        
    def post(self):
        session_name = self.request.get("session_name")
        date = self.request.get("date")
        start_timeval = self.request.get("start_time")
        end_timeval = self.request.get("end_time")
        
        start = date + " " + start_timeval
        start_timedate = time.strptime(start, "%Y-%m-%d %H:%M")
        end = date + " " + end_timeval
        end_timedate = time.strptime(end, "%Y-%m-%d %H:%M")

        session_location=self.request.get("session_location")
        session_description=self.request.get("session_description")
        session_speakers=self.request.get("speakers")
        session_biography=self.request.get("biography")
        survey_link=self.request.get("survey_link")

        
        session1 = Session(name=session_name,
                           description=session_description,
                           location=session_location,
                           parent=ndb.Key('Type', 'Session', 'Name', session_name),
                           start_date=datetime.datetime.fromtimestamp(mktime(start_timedate)),
                           end_date=datetime.datetime.fromtimestamp(mktime(end_timedate)),
                           speakers=session_speakers,
                           biography=session_biography,
                           survey=survey_link)
        session1.put()
        self.response.write('stored!')

class DataHandler(webapp2.RequestHandler):


    def get(self):
        session_query = Session.query(ancestor=ndb.Key('Type', 'Session'))
        session = session_query.fetch(100)
        
        self.response.write('Current sessions: ' +  '<br/>')

        for s in session:
            
            self.response.write('Name: ' + noNone(s.name) + '<br/>' +
                                'Decription: ' + noNone(s.description) + '<br/>' +
                                'Location: ' + noNone(s.location) + '<br/>' +
                                'Speaker(s): ' + noNone(s.speakers) + '<br/>' +
                                'Biography: ' + noNone(s.biography) + '<br/>' +
                                'Survey Link: ' + noNone(s.survey) + '<br/>' +
                                'Start Time: ' + noNoneDate(s.start_date) + '<br/>'
                                'End Time: ' + noNoneDate(s.end_date) +  
                                delete_form_create(s.name) + '<br/> <br/>' )




class DeleteHandler(webapp2.RequestHandler):
    

    def post(self):
        key = ndb.Key('Type', 'Session', 'Name', self.request.get("key"))
        session_query = Session.query(ancestor=key)
        
        sessions = session_query.fetch(100)
        
        for s in sessions:
            self.response.write('Deleted: ' + s.name + '<br/>')
            s.key.delete()


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


class jsonHandler(webapp2.RequestHandler):

    def get(self):
      key = ndb.Key('Type', 'Session')
      session_query = Session.query(ancestor=key)
        
      sessions = session_query.fetch(100)
      string_json = "["
      for s in sessions:
        string_json = string_json + json.dumps({"session_name" : s.name, "location" : s.location,
                    "stime" : str(s.start_date), "edate" : str(s.end_date) }) + ","

      string_json = string_json[0:-1] + "]"

      self.response.write(string_json)






app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/data', DataHandler),
    ('/delete', DeleteHandler),
    ('/machine.json' , jsonHandler)
], debug=True)


