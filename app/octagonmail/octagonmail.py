import re
import smtplib
from email.message import EmailMessage
import email.message
import mimetypes
from typing import Dict

send_address = "noreply.octagon@gmail.com"
passs = "-"

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
