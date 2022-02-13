import ssl
import socket
import datetime, smtplib
import json
import sys
import random
import requests

def send_notification(daysToExpiration,hostname):
    day=str(daysToExpiration)
    url = "Paste you slack channel webhook URL"
    message = ("Hostname : "+hostname)
    title = ("SSL Certificate will expire within "+day+" days")
    slack_data = {
    "username": "SSL-Certificate-Expiry",
    "icon_emoji": ":satellite:",
    #"channel" : "#somerandomcahnnel",
    "attachments": [
        {
            "color": "#9733EE",
            "fields": [
                {
                    "title": title,
                    "value": message,
                    "short": "false",
                }
            ]
        }
    ]
    }
    byte_length = str(sys.getsizeof(slack_data))
    headers = {'Content-Type': "application/json", 'Content-Length': byte_length}
    response = requests.post(url, data=json.dumps(slack_data), headers=headers)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    #print(daysToExpiration)

hostname = ['stark-yv.github.io'] #add all your host name here
port = '443'
for i in hostname:
    context = ssl.create_default_context()
    with socket.create_connection((i, port)) as sock:
        with context.wrap_socket(sock, server_hostname = i) as ssock:
            certificate = ssock.getpeercert()

    certExpires = datetime.datetime.strptime(certificate['notAfter'], '%b %d %H:%M:%S %Y %Z')
    daysToExpiration = (certExpires - datetime.datetime.now()).days
    #print(daysToExpiration,i)
    if daysToExpiration <= 18 or daysToExpiration<= 15:
        send_notification(daysToExpiration,i)
