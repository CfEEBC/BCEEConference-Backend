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


MAIN_PAGE_FOOTER_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
<title>BCEE Conference App</title>
<script>
function validateForms() {
var location = document.forms['addSessionForm']['session_location'].value;
var description = document.forms['addSessionForm']['session_description'].value;
var speakers = document.forms['addSessionForm']['speakers'].value;
var biography = document.forms['addSessionForm']['biography'].value;
var survey_link = document.forms['addSessionForm']['survey_link'].value;
var name = document.forms['addSessionForm']['session_name'].value;
var date = document.forms['addSessionForm']['date'].value;
var start_time = document.forms['addSessionForm']['start_time'].value;
var end_time = document.forms['addSessionForm']['end_time'].value;

if (location == null || location == "") {
    alert("Please enter a location");
    return false;
} else if (description == null || description == "") {
    alert("Please enter a description");
    return false;
} else if (speakers == null || speakers == "") {
    alert("Please enter a list of speakers");
    return false;
} else if (biography == null || biography == "") {
    alert("Please enter a biography");
    return false;
} else if (survey_link == null || survey_link == "") {
    alert("Please enter a survey link");
    return false;
} else if (name == null || name == "") {
    alert("Please enter a name");
    return false;
} else if (date == null || date == "") {
    alert("Please specify a date");
    return false;
} else if (start_time == null || start_time == "") {
    alert("Please specify a starting time");
    return false;
} else if (end_time == null || end_time == "") {
    alert("Please specify an ending time");
    return false;
} else {
    return true;
}
}
</script>
</head>

<body>
    <form action="/" method="post" name="addSessionForm" onsubmit="return validateForms()">
      Session Location
      <div><textarea name="session_location" rows="3" cols="60"></textarea></div>
      Session Description
      <div><textarea name="session_description" rows="3" cols="60"></textarea></div>
      Session Speaker(s)
      <div><textarea name="speakers" rows="1" cols="60"></textarea></div>
      Biography
      <div><textarea name="biography" rows="3" cols="60"></textarea></div>
      Survey Link
      <div><textarea name="survey_link" rows="1" cols="60"></textarea></div>
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
def delete_form_create(session_name):
        delete_form = """<form action="/delete" method="post">
        <input type="hidden" name="key" value="%s">
        <input type="submit" value="Delete"></form>""" % session_name
        return delete_form

class MainHandler(webapp2.RequestHandler):

    def get(self):
        self.response.write(MAIN_PAGE_FOOTER_TEMPLATE)
        
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





app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/data', DataHandler),
    ('/delete', DeleteHandler)
], debug=True)


