#********
# Python Script to call the Atlasian JIRA Rest API.
# Detailed documentation - https://confluence.renesas.com/display/GMANUF/JIRA+Automation
#
# curl -u username:password -X GET --insecure "https://jira.global.renesas.com/rest/api/2/myself"
# curl -u jiraadm_internal:SVY7sj37ssW9 -X GET --insecure "https://jira.global.renesas.com/rest/api/2/myself"
# 
# curl -u username:password -X GET --insecure -H "Content-Type: application/json" "https://jira.global.renesas.com/rest/api/2/search?jql=project=%22GYM%22%20AND%20status=Done%20AND%20issuetype=%22Sub-task%22"
# curl -u jiraadm_internal:SVY7sj37ssW9 -X GET --insecure -H "Content-Type: application/json" "https://jira.global.renesas.com/rest/api/2/search?jql=project=%22GYM%22%20AND%20status=Done%20AND%20issuetype=%22Sub-task%22"
#
# Script Execution steps -
# C:\Users\a5143522\CodeBase\automation_jobs\automation_jobs>python email_user_jira_task.py
# Enter assignees' emails separated by commas: # Sany.Singh@diasemi.com,Paulo.Safaro@diasemi.com,chris.baptist.eb@renesas.com,ahamad.shaik.vf@renesas.com,Tasos.Dekazos@diasemi.com
# C:\Users\a5143522\AppData\Local\Programs\Python\Python312\Lib\site-packages\urllib3\connectionpool.py:1103: InsecureRequestWarning: Unverified HTTPS request is being made to host 'jira.global.renesas.com'. Adding certificate verification is strongly advised. See: https://urllib3.readthedocs.io/en/latest/advanced-usage.html#tls-warnings
#  warnings.warn(
# Report sent successfully via email.
# C:\Users\a5143522\CodeBase\automation_jobs\automation_jobs>
#
#*********
import requests
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Define Jira credentials and base URL
USERNAME = 'jiraadm_internal'
PASSWORD = 'SVY7sj37ssW9'
JIRA_URL = 'https://jira.global.renesas.com/rest/api/2/search'

# Get today's date
today = datetime.date.today()
# Calculate the date 7 days ago
seven_days_ago = today - datetime.timedelta(days=7)
# Construct the date string in the format required by JIRA (YYYY-MM-DD)
seven_days_ago_str = seven_days_ago.strftime('%Y-%m-%d')

# Prompt the user to enter assignees' emails separated by commas
# Sany.Singh@diasemi.com,Paulo.Safaro@diasemi.com,chris.baptist.eb@renesas.com,ahamad.shaik.vf@renesas.com,Tasos.Dekazos@diasemi.com
assignees_emails_str = input("Enter assignees' emails separated by commas: ")

# Split the input string into a list of emails
assignees_emails = [email.strip() for email in assignees_emails_str.split(',')]

# Construct JQL query to find finished development tasks for assignees' emails
JQL_QUERY = f'project = "GYM" AND status = Done AND issuetype = "Sub-task" AND assignee in ({", ".join([f"\"{email}\"" for email in assignees_emails])}) AND resolutiondate >= {seven_days_ago_str}'

# Specify the fields to retrieve
FIELDS = 'assignee,key,summary,resolutiondate'

# Construct authentication header
auth_header = (USERNAME, PASSWORD)

# Define parameters for the API call
params = {
    'jql': JQL_QUERY,
    'fields': FIELDS
}

# Make the API call
response = requests.get(JIRA_URL, params=params, auth=auth_header, verify=False)

# Check if the request was successful
if response.status_code == 200:
    # Parse JSON response
    data = response.json()
    
    # Extract key, summary, and assignee's email from each issue
    issues_info = []
    for issue in data['issues']:
        key = issue['key']
        summary = issue['fields']['summary']
        assignee_email = issue['fields']['assignee']['emailAddress']
        issues_info.append((key, summary, assignee_email))
    
    # Format the issues information into a readable format
    report_text = "\n".join([f"Key: {key}\nSummary: {summary}\nAssignee: {assignee_email}\n" for key, summary, assignee_email in issues_info])
    
    # Send the report via email
    sender_email = 'noreply@renesas.com'  # Update with sender's email
    to_recipients = ['chris.baptist.eb@renesas.com']  # Recipients in "To" field
    cc_recipients = ['sany.singh.xm@renesas.com']  # Recipients in "Cc" field
    
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = ', '.join(to_recipients)  # Comma-separated list of "To" recipients
    message['Cc'] = ', '.join(cc_recipients)  # Comma-separated list of "Cc" recipients
    receiver_email = to_recipients + cc_recipients  # Combine "To" and "Cc" recipients
    message['Subject'] = 'Weekly Jira Report'

    # Add report text to the email body
    message.attach(MIMEText(report_text, 'plain'))

    # Connect to the SMTP server and send the email
    with smtplib.SMTP('mail.idc.renesas.com', 25) as server:  # Update with your SMTP server details
        server.sendmail(sender_email, receiver_email, message.as_string())

    print("Report sent successfully via email.")
else:
    print(f"Failed to retrieve data. Status code: {response.status_code}")



