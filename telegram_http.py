#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Sebastian Porteiro 2017-19 jporteiro@iter.es
#Listen to PORT_NUMBER and send a Telegram message using bot
import sys, os
import gi
import subprocess
import time
import datetime
import threading
import json
import hashlib
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import telegram
from telegram.error import NetworkError, Unauthorized
from time import sleep
#for post requests
import requests
import base64

HOST_NAME = '0.0.0.0'
PORT_NUMBER = 8082 #any available port
TOKEN = '96144d11f8fec9a5636fa85460c493da809c1f259728ee8da371fb4d' #hashlib.sha224("userpass").hexdigest()
TOKEN_BOT = 'CREATEABOTFIRSTANDPASTETOKENHERE'
CHAT_ID = 00000000000 #conversation ID to which you want to send the messages

class httpServerBot(BaseHTTPRequestHandler):
    def do_POST(self):
        paths = {
            '/msg': {'status': 200,'Content-type':'text/html'}
        }
        if self.path in paths:
            self.respond(paths[self.path])
        else:
            self.respond({'status': 500,'Content-type':'text/html'})

    def handle_http(self, status_code, path):
        self.send_response(status_code)
        #should be called like curl -X POST -d '{"user":"user","pass":"pass","msg":"Message"}'  http://localhost:8082/msg
        if path == '/msg':
            #print(self.headers)
            try:
                length = int(self.headers.get('content-length'))
                post_body = self.rfile.read(length)
                post_body = post_body.decode('UTF-8')
                post_body = json.loads(post_body)
                userAndPassword = str(post_body['user']+post_body['pass'])
                userAndPassword = userAndPassword.encode('utf8')
                userAndPassword = hashlib.sha224(userAndPassword).hexdigest()
                if userAndPassword == TOKEN:
                    self.run_bot('telegram_http.py: ' + str(post_body['msg'].encode('utf8')))
                    contents = 'Message has been sent'
                else:
                    contents = 'Not Authorized'
            except:
                print('Unable to process, check user and pass or bot not available')
                contents = 'Unable to process, check user and pass or bot not available'

        return bytes(contents)

    def respond(self, opts):
        response = self.handle_http(opts['status'], self.path)
        self.send_header('Content-type',opts['Content-type'])
        self.end_headers()
        self.wfile.write(response)

    def get_path(self):
        return os.path.dirname(os.path.realpath(__file__))

    def run_bot(self,msg):
        global update_id
        bot = telegram.Bot(TOKEN_BOT)
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        bot.send_message(chat_id=CHAT_ID, text=msg)

if __name__ == '__main__':
    server_class = HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), httpServerBot)
    print('['+ datetime.datetime.now().strftime("%A, %d. %B %Y %H:%M%p:%S%p")+']', 'Web server listening - %s:%s' % (HOST_NAME, PORT_NUMBER))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print('['+ datetime.datetime.now().strftime("%A, %d. %B %Y %H:%M%p:%S%p")+']', 'Web server stops - %s:%s' % (HOST_NAME, PORT_NUMBER))
