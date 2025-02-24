import os
import sys
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import config as c
from datetime import datetime

datetime_now = (datetime.now()).strftime("%y%m%d%H%M")


#todo : Define the scope
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

# Path to the credentials file
credentials_file = 'credentials.json'
user_name = 'aws.ccp21@gmail.com' # user for msg_from too.
user_pwd = c.API_KEY_CS
recipient_email = 'aws.ccp21@gmail.com'
cc_emails = ['aws.ccp21@gmail.com']


# Check if credentials file exists
if not os.path.exists(credentials_file):
    print("Credentials file not found.")
    sys.exit()

# Load credentials from the file
creds = None
if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(credentials_file, SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.json', 'w') as token:
        token.write(creds.to_json())

# Create the email message
msg = MIMEMultipart()
msg['From'] = user_name
recipient_email = recipient_email
cc_emails = cc_emails
msg['To'] = recipient_email
msg['Cc'] = ', '.join(cc_emails)
msg['Subject'] = f'Test Email : {datetime_now}'

msg.attach(MIMEText(f'Hello\n\n\nThis is a test email at {datetime_now}. \n\n\nRegards\nCS_Team', 'plain'))

# Connect to Gmail's SMTP server
server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
# server.login('aws.ccp21@gmail.com', creds.token)
server.login(user_name, user_pwd)
all_recipients = [recipient_email] + cc_emails
server.sendmail(msg['From'], all_recipients, msg.as_string())
server.quit()

print("Email sent successfully!")
