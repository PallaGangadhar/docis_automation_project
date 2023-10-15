import smtplib
import os
from os.path import join, dirname
from dotenv import load_dotenv
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

SENDER_MAIL=os.environ.get('SENDER_MAIL')
SENDER_PASSWORD=os.environ.get('SENDER_PASSWORD')

def send_mail_to(content):
    print("Content===",content)
    message=None
    with open("static/files/abc.txt","r") as f:
        message=f.readlines()
    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)
    
    # start TLS for security
    s.starttls()
    
    # Authentication
    s.login(SENDER_MAIL, SENDER_PASSWORD)
    message_text=""
    for data in message:
        message_text+=data+"\n"

    message_to_be_send = 'Subject: {}\n\n{}'.format("Summary Table", message_text)
    # message to be sent
    # message = message
    # sending the mail
    s.sendmail(SENDER_MAIL, "ganga11497@gmail.com", message_to_be_send)
    
    # terminating the session
    # s.quit()

# import smtplib

# body = 'Subject: Subject Here .\nDear ContactName, \n\n' + 'Email\'s BODY text' + '\nYour :: Signature/Innitials'
# try:
#     smtpObj = smtplib.SMTP('smtp-mail.outlook.com', 587)
# except Exception as e:
#     print(e)
#     smtpObj = smtplib.SMTP_SSL('smtp-mail.outlook.com', 465)
# #type(smtpObj) 
# smtpObj.ehlo()
# smtpObj.starttls()
# smtpObj.login(SENDER_MAIL,SENDER_PASSWORD) 
# smtpObj.sendmail(SENDER_MAIL, SENDER_MAIL, body) # Or recipient@outlook

# smtpObj.quit()
