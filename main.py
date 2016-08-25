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
import re

page_header = """
<!DOCTYPE html>
<html>
<head>
    <title>User Signup</title>
</head>
<body>
    <h1>User Signup</h1>
"""

page_footer = """
</body>
</html>
"""

validate_form = """
<form action ="/validate_form" method ="post">
    <label>Username</label>
        <input type ="text" name ="username" value ="%(username)s"/>
        <div style ="color: red; display:inline;">%(username_error)s</div>
        <br>
    <label>Password</label>
        <input type ="password" name ="password" value ="%(password)s" />
        <div style = "color: red; display:inline;">%(password_error)s</div>
        <br>
    <label>Verify</label>
        <input type ="password" name ="verify" value ="%(verify)s"/>
        <div style ="color: red; display:inline;">%(verify_error)s</div>
        <br>
    <label>Email (optional)</label>
        <input type ="text" name ="email" value ="%(email)s"/>
        <div style ="color: red; display:inline;">%(email_error)s</div>
        <br>
        <input type ="submit"/>
</form>
"""
USER_RE = re.compile(r"^[a-zA-z0-9_-]{3,20}$")
def valid_username(username):
    return USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return PASS_RE.match(password)

EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
def valid_email(email):
    return EMAIL_RE.match(email)

class MainHandler(webapp2.RequestHandler):
    def write_form(self, username_error="", password_error="", verify_error="",
                    email_error="", username="", password="", verify="", email=""):
        self.response.write(page_header + validate_form % {"username_error": username_error,
                                            "password_error": password_error,
                                            "verify_error": verify_error,
                                            "email_error": email_error,
                                            "username": username,
                                            "password": password,
                                            "verify": verify,
                                            "email": email} + page_footer)
    def get(self):
        self.write_form()

class Validation(webapp2.RequestHandler):
    def write_form(self, username_error="", password_error="", verify_error="",
                    email_error="", username="", email=""):
        self.response.write(page_header + validate_form % {"username_error": username_error,
                                            "password_error": password_error,
                                            "verify_error": verify_error,
                                            "email_error": email_error,
                                            "username": username,
                                            "password": "",
                                            "verify": "",
                                            "email": email} + page_footer)
    def post(self):

        client_username = self.request.get('username')
        client_password = self.request.get('password')
        client_verify = self.request.get('verify')
        client_email = self.request.get('email')

        valid_u_name = valid_username(client_username)
        valid_pass = valid_password(client_password)
        valid_e = valid_email(client_email)

        if not (valid_pass):
            self.write_form(password_error="That's not a valid password.", username=client_username, email=client_email)

        elif not (valid_u_name):
            self.write_form(username_error="That's not a valid username.", username=client_username, email=client_email)

        elif not(valid_e) and len(client_email) != 0:
            self.write_form(email_error="That's not a valid email.", username=client_username, email=client_email)

        elif client_password != client_verify:
            self.write_form(verify_error="Passwords do not match.", username=client_username, email=client_email)

        else:
            self.response.out.write("<h1>Welcome " + client_username + "!</h1>")

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/validate_form', Validation)
], debug=True)
