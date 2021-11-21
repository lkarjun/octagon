import re
import smtplib
import email.message
import mimetypes

send_address = "-"
passs = "-"

def send_email(to: str, subject) -> int:
    """ for sending report """
    try:
        message = email.message.EmailMessage()
        message["From"] = "noreply.octagon@gmail.com"
        message["to"] = to
        message["Subject"] = subject
        body = "Kindly Please check Your system, and resolve it."
        message.set_content(body)
        mail_server = smtplib.SMTP_SSL('smtp.gmail.com')

        """ to loading some credential """
        
        mail_server.login(send_address, passs)
        mail_server.send_message(message)
        mail_server.quit()
        return 0
    except:
        return 1
