import re
import smtplib
import email.message
import mimetypes
from typing import Dict

send_address = "-"
passs = "-"

def send_email(data: Dict) -> int:
    """ for sending report """
    try:
        message = email.message.EmailMessage()
        message["From"] = send_address
        message["to"] = data['to']
        message["Subject"] = data['subject']
        message.set_content(data['body'])
        mail_server = smtplib.SMTP_SSL('smtp.gmail.com')

        """ to loading some credential """
        
        mail_server.login(send_address, passs)
        mail_server.send_message(message)
        mail_server.quit()
        return 0
    except:
        return 1
