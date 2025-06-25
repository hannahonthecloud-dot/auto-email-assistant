# ==========================
# Step 1: Authenticate with Google APIs
# ==========================

import os
import base64
from email.mime.text import MIMEText
from email.message import EmailMessage


# Import necessary libraries for Google API authentication
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

#Import necessary libraries to send email with attachments from gmail
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage

# Import necessary libraries for Google Sheets
import gspread
from oauth2client.service_account import ServiceAccountCredentials



CLIENT_SECRET_FILE = '/home/admin-hannah/G-mail-script/client_secret_101.json'
SCOPES = [
    'https://mail.google.com/',
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

creds = None
# The file token.json stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)

# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            CLIENT_SECRET_FILE, SCOPES)
        
        # Uncomment the next line to use the local server flow
        creds = flow.run_local_server(port=0)
        # Uncomment the next line to use the console flow
        # flow.run_console()
        # Uncomment the next line to use the manual authorization flow
        # Note: The manual authorization flow requires user interaction to
        # authorize the application and obtain the authorization code.
        # This is useful for environments where a web browser is not available.

        # Manual authorization flow. Uncomment this part if running on WSL
        # flow.redirect_uri = 'urn:ietf:wg:oauth:2.0:oob'
        # auth_url, _ = flow.authorization_url(prompt='consent')
        # print(f"Please go to this URL: {auth_url}")
        # code = input("Enter the authorization code: ")
        # flow.fetch_token(code=code)

        creds = flow.credentials

    # Save the credentials for the next run
    with open('token.json', 'w') as token:
        token.write(creds.to_json())

service_gmail = build('gmail', 'v1', credentials=creds)

# ==========================
# Step 2: Connect to Google Sheet
# ==========================

# Make sure you've enabled Google Sheets API in Google Cloud Console
# Use the same Gmail OAuth credentials to authorize Sheets
gspread_client = gspread.authorize(creds)


# Open your Google Sheet by name
sheet = gspread_client.open("JOB TRACKING").sheet1  # Replace with your actual sheet name


# Get all values from the sheet
all_values = sheet.get_all_values()

# Look for the header row containing required fields
expected_headers = {'company', 'role', 'recruiter email', 'email type', 'sent', 'recruiter name'}
header_row_index = None

for i, row in enumerate(all_values):
    row_cleaned = [cell.strip().lower() for cell in row]
    if expected_headers.issubset(set(row_cleaned)):
        header_row_index = i + 1  # gspread uses 1-based indexing
        break

if header_row_index is None:
    raise ValueError(" Couldn't find a row with all required headers.")

# Now get all records starting from that row
# Get all rows as dictionaries
raw_rows = sheet.get_all_records(head=header_row_index)

# Normalize all keys in every row to lowercase
rows = [
        {k.lower(): v for k, v in row.items()} 
        for row in raw_rows]


# ==========================
# Step 3: Define Simple Email Creation Function
# ==========================

def create_message(sender, to, subject, message_text):
    """Create a raw email message for the Gmail API."""
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return {'raw': raw}


# ==========================
# Step 4: Loop and Send Emails (No Attachments)
# ==========================

for index, row in enumerate(rows, start=5):  # Start at row 5 to skip header

    # Only send if Sent? column is "No"
    if row['sent'].strip().lower() != 'no':
        continue

    # Choose template file
    email_type = row['email type'].strip().lower()
    if email_type == 'thank-you':
        template_path = 'templates/Thank-you.txt'
    elif email_type == 'follow-up':
        template_path = 'templates/Follow-up.txt'
    else:
        print(f" Unknown email type in row {index}")
        continue

    # Load and fill template
    # Load template
    with open(template_path, 'r') as file:
        template = file.read()

    # Extract subject from first line
    template_lines = template.splitlines()
    subject_line = template_lines[0].strip()

    if subject_line.lower().startswith("subject:"):
        
        # Extract subject line and replace placeholders
        # Assuming subject line starts with "Subject: "
        subject_template = (
    subject_line[8:].strip()
                   .replace('{{company}}', row['company'])
                   .replace('{{role}}', row['role'])
                   .replace('{{recruiter_name}}', row['recruiter name'])
)

    else:
        subject_template = f"Regarding the {row['role']} role at {row['company']}"  # Fallback

    # Prepare email body (everything after subject line)
    body_template = '\n'.join(template_lines[1:])
    personalized_body = (
        body_template.replace('{{company}}', row['company'])
                     .replace('{{role}}', row['role'])
                     .replace('{{recruiter_name}}', row['recruiter name'])
    )

    # Email details
    to = row['recruiter email']


    try:
        print(f" Sending to {to}...")
        message = create_message("me", to, subject_template, personalized_body)
        service_gmail.users().messages().send(userId="me", body=message).execute()

        # Mark as sent in sheet
        sheet.update_cell(index, 7, 'Yes')  # Assumes column 7 is "Sent"
        print(f" Sent and updated row {index}")

    except Exception as e:
        print(f" Error sending to {to} in row {index}: {e}")


# ==========================
# Done
# ==========================
print("All emails processed.")