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
import hmac

secret = 'ASPOIUlsf;asf[gjdksl'
password = "password"
hashed_password = hmac.new(secret, "password").hexdigest()



JINJA_ENVIRONMENT = jinja2.Environment(
        loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
        extensions=['jinja2.ext.autoescape'],
        autoescape=True)

class MainHandler(webapp2.RequestHandler):

    def get(self):
        cookies = self.request.cookies

        if (("admin" in cookies) and 
            cookies["admin"] == make_secure_val("admin", password)):
            template_values = {}

            template = JINJA_ENVIRONMENT.get_template('index.html')
            self.response.write(template.render(template_values))
        else:
            
            self.redirect('/')

        
    def post(self):
        addSession(self)

def addSession(caller):
    session_name = caller.request.get("session_name")
    date = caller.request.get("date")
    start_timeval = caller.request.get("start_time")
    end_timeval = caller.request.get("end_time")
    
    start = date + " " + start_timeval
    start_timedate = time.strptime(start, "%Y-%m-%d %H:%M")
    end = date + " " + end_timeval
    end_timedate = time.strptime(end, "%Y-%m-%d %H:%M")

    session_location=caller.request.get("session_location")
    session_description=caller.request.get("session_description")
    session_speakers=caller.request.get("speakers")
    session_biography=caller.request.get("biography")
    survey_link=caller.request.get("survey_link")

    
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

    template_values = {}
    template = JINJA_ENVIRONMENT.get_template('confirm.html')
    caller.response.write(template.render(template_values))

class DataHandler(webapp2.RequestHandler):

    def get(self):
        cookies = self.request.cookies
        if (("admin" in cookies) and cookies["admin"] == make_secure_val("admin", password)):
            
            session_query = Session.query(ancestor=ndb.Key('Type', 'Session'))
            session = session_query.fetch(100)
        
            self.response.write('Current sessions: ' +  '<br/>')
        
            session_list = []
            for s in session:
                session_dict = {
                            'Name':noNone(s.name),
                            'Decription': noNone(s.description),
                            'Location':noNone(s.location),
                            'Speakers':noNone(s.speakers),
                            'Biography':noNone(s.biography),
                            'Survey':noNone(s.survey),
                            'Start':noNoneDate(s.start_date),
                            'End':noNoneDate(s.end_date)
                            }
                session_list.append(session_dict)
        
            template_values = {
                        'sessions':session_list}

            template = JINJA_ENVIRONMENT.get_template('data.html')
            self.response.write(template.render(template_values))

        else:
            self.redirect('/')



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
                    "stime" : str(s.start_date), "etime" : str(s.end_date),
                    "description" : s.description, "speakers" : s.speakers,
                    "biography" : s.biography, "survey_link" : s.survey }) + ","

      string_json = string_json[0:-1] + "]"

      self.response.write(string_json)


def make_secure_val(val, password):
    return '%s|%s' % (val, hmac.new(secret, val).hexdigest())

class Login(webapp2.RequestHandler):
    def get(self):
        template_values = {}
        template = JINJA_ENVIRONMENT.get_template('login-form.html')
        self.response.write(template.render(template_values))
        

    def post(self):
        
        password_log = self.request.get('password')

        
        if hmac.new(secret,password_log).hexdigest() == hashed_password :
            cookie_val = make_secure_val("admin",password_log)
            self.response.headers.add_header(
            'Set-Cookie',
            str('%s=%s; Path=/' % ("admin", cookie_val)))
            self.redirect('/add')
        else:
            msg = 'Invalid login'
            template_values = {"error" : msg}
            template = JINJA_ENVIRONMENT.get_template('login-form.html')
            self.response.write(template.render(template_values))

class EditHandler(webapp2.RequestHandler):
    def post(self):
        session_name = self.request.get('key')
        key = ndb.Key('Type', 'Session', 'Name', session_name)
        
        session_query = Session.query(ancestor=key)
        session = (session_query.fetch(1))[0]
        
        template_values = {
            'prior_name':session.name,
            'submit_target':'/editProcessor',
            'prefill_location':session.location,
            'prefill_description':session.description,
            'prefill_speakers':session.speakers,
            'prefill_biography':session.biography,
            'prefill_survey':session.survey,
            'prefill_name':session.name
        }
        
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))

class EditProcessor(webapp2.RequestHandler):
    def post(self):
        old_key = ndb.Key('Type', 'Session', 'Name', self.request.get('prior_name'))
        session_query = Session.query(ancestor=old_key)
        session = (session_query.fetch(1))[0]
        session.key.delete()
        
        addSession(self)
        
        
        
app = webapp2.WSGIApplication([
    ('/add', MainHandler),
    ('/data', DataHandler),
    ('/delete', DeleteHandler),
    ('/machine' , jsonHandler),
    ('/edit', EditHandler),
    ('/editProcessor', EditProcessor),
    ('/' , Login)
], debug=True)


