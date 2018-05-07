#! /usr/bin/python3

import json
import requests
import smtplib

from email.message import EmailMessage
from gunicorn.app.wsgiapp import WSGIApplication

class ThirdHead:
    """
    Third Head : Barking.
    
    Alert using external server.
    """
    def __init__(
        self,
        app,
        email_host='localhost',
        email_port=None,
        email_login=None,
        email_password=None,
        email_recipients=None,
        *args,
        **kwargs
    ):
        self.app = self.start_webserver()
        self.base_url = 'http://localhost:8000/'
        self.email_host = email_host        
        self.email_login = email_login
        self.email_password = email_password
        self.email_recipients = email_recipents
        self.request = self.get_requests_session()
	
    def start_webserver(self):
        app = WSGIApplication()
        app.app_uri = 'cerberus.webserver:app'
        return app.run()

    def get_requests_session():
        # Not really useful for the moment, but could be in the future with Auth system
        return requests.Session()

    def update_status(self, new_status):
        self.request.post(self.base_url + 'cerberus_status', json.dumps({'status': new_status}))
		
    def new_detection(self):
        self.request.post(self.base_url + 'new_detection')
        self.request.post(self.base_url + 'detection_amount')
        self.bark()
        self.update_status('Intruder has been spotted !')
        
    def bark(self):
        # Create message
        msg = EmailMessage()
        msg['From'] = 'cerberus@localhost'
        msg['To'] = self.recipients
        msg['Subject'] = 'New alert'
        msg.set_content('An intruder has been spotted !')

        # Barking !
        with smtplib.SMTP(self.email_host, self.email_port) as smtp_server:
            if self.email_login and self.email_password:
                smtp_server.ehlo()
                smtp_server.starttls()
                smtp_server.login(self.email_login, self.email_password)
            finally:
                smtp_server.send_message(msg)
