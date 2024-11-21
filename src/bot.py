import email, smtplib, ssl

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.core.mail import EmailMultiAlternatives
from core.settings import MEDIA_ROOT, EMAIL_HOST_USER
import threading

def send_email_thread(receiver,subject,content,mail_id, attachment):
    if type(receiver) == list:
        msg = EmailMultiAlternatives(subject, "", mail_id, receiver)
    else:
        msg = EmailMultiAlternatives(subject, "", mail_id, [receiver])
    msg.attach_alternative(content, "text/html")
    if attachment is not None:
        msg.attach_file(attachment)
    msg.send()

class EmailBotClass:
    def __init__(self,mail_id):
        self.port = 587  # For starttls #465
        self.smtp_server = "smtp.live.com" #mail.privateemail.com
        self.mail_id = mail_id
       
    def send_email(self, client_email, client_name, subject, title, content, **kwargs):
        body_content = '\
                <p style="text-align:center;color:orange;font-size: 36px;"><b> '+title+' </b></p><hr>\
                <p> Dear <b>'+client_name+'</b><br><br><br>\
                '+content+'<br><hr>\
                Thanks for choosing CSWMS, wish you have a great day.<br>\
                Support Email : <b>assessment</b>\
            '
        attachment = kwargs.get("attachment")
        x = threading.Thread(target=send_email_thread, args=(client_email,subject,body_content,self.mail_id,attachment))
        x.start()

        
EmailBot = EmailBotClass(EMAIL_HOST_USER)

