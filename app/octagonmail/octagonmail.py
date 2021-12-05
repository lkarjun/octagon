import re
import smtplib
from email.message import EmailMessage
import email.message
import mimetypes
from typing import Dict
from octagonmail.mail_template import *

send_address = "noreply.octagon@gmail.com"
passs = "Project@2021"

def get_message(data: Dict) -> EmailMessage:
    """ for sending report """
    message = EmailMessage()
    message["From"] = send_address
    message["to"] = data['to']
    message["Subject"] = data['subject']
    message.set_content(data['body'], subtype=data['subtype'])
    return message

def send_mail(message: EmailMessage) -> bool:
    """ sending mail """
    try:
        mail_server = smtplib.SMTP_SSL('smtp.gmail.com')
        mail_server.login(send_address, passs)
        mail_server.send_message(message)
        mail_server.quit()
        return True
    except:
        return False

def verification_mail(name: str, email: str, id: str):
    id = f"http://127.0.0.1:8000/verify/{id}"
    html = html_head.format(body=verification_template.format(name=name.upper(), link=id))
    data = {'subject': 'Verification Needed',
            'subtype': 'html',
            'to': email,
            'body': html}
    print(send_mail(get_message(data)))


def greeting_mail(username: str, name: str, email: str):
    print("Greeting is sended")
    link = f"http://127.0.0.1.8000"
    html = html_head.format(body=greeting_template.format(name=name, username=username, email=email, link=link))
    data = {'subject': 'Verification Completed',
            'subtype': 'html',
            'to': email,
            'body': html}

    print(send_mail(get_message(data)))