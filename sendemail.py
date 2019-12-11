#!/usr/bin/env python
#Sebastian Porteiro 2017-19 jporteiro@iter.es
#Import everything we need
import sys, os
import time
import datetime
import smtplib
import subprocess
#for sending emails
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
settings = {
	"email_from" : "user@server.com",
	"email_pass" : "secret",
	"email_port" : 587,
	"email_server" : "smtp.server.com",
	"email_to" : "destination@server.com",
	"email_user" : "user"
}
#Made for calling it from another script/console, parameter required is the subject
def send_email(message=sys.argv[1]):
    try:
        hostname =  subprocess.Popen("hostname", shell=True, stdout=subprocess.PIPE)
        hostname = hostname.stdout.read().decode("utf-8").rstrip()
        msg = MIMEMultipart()
        msg['From'] = settings['email_from']
        msg['To'] = str('"'+settings['email_to']+'"')
        msg['Subject'] = "Email from: " + hostname
        email_to_list = settings['email_to'].split(",")
        body = message
        msg.attach(MIMEText(body, 'plain'))
        server = smtplib.SMTP(settings['email_server'],settings['email_port'])
        server.starttls()
        server.login(settings['email_user'], settings['email_pass'])
        text = msg.as_string()
        server.sendmail(settings['email_from'], email_to_list, text)
        server.quit()
        print('SEND EMAIL: email has been sent to ' + msg['To'])
    except:
        print('SEND EMAIL: email cannot be send')
send_email()
#testing
