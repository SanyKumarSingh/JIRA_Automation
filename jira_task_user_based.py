#********
# Python Script to call the Atlasian JIRA Rest API.
# Detailed documentation - https://confluence.renesas.com/display/GMANUF/JIRA+Automation
#
# C:\Users\a5143522\CodeBase\PythonJobs>python jira_task_count.py
#
# curl -u username:password -X GET --insecure "https://jira.global.renesas.com/rest/api/2/myself"
# curl -u jiraadm_internal:SVY7sj37ssW9 -X GET --insecure "https://jira.global.renesas.com/rest/api/2/myself"
# 
# curl -u username:password -X GET --insecure -H "Content-Type: application/json" "https://jira.global.renesas.com/rest/api/2/search?jql=project=%22GYM%22%20AND%20status=Done%20AND%20issuetype=%22Sub-task%22"
# curl -u jiraadm_internal:SVY7sj37ssW9 -X GET --insecure -H "Content-Type: application/json" "https://jira.global.renesas.com/rest/api/2/search?jql=project=%22GYM%22%20AND%20status=Done%20AND%20issuetype=%22Sub-task%22"
#
#*********
import requests
import datetime

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
assignees_emails_str = input("Enter assignees' emails separated by commas: ")

# Split the input string into a list of emails
# Sany.Singh@diasemi.com,Paulo.Safaro@diasemi.com,chris.baptist.eb@renesas.com,ahamad.shaik.vf@renesas.com,Tasos.Dekazos@diasemi.com
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
    
    # Print count of finished development tasks
    total_count = data.get('total', 0)
    print(f"Total count of finished development tasks: {total_count}")
    
    # Save JSON response to a file
    with open('jira_data.json', 'w') as f:
        f.write(response.text)
    print("JSON data saved to 'jira_data.json' file.")
    
    # Filter issues based on assignees' emails
    for email in assignees_emails:
        filtered_issues = [issue for issue in data['issues'] if issue['fields']['assignee']['emailAddress'] == email]
        
        # Print count of finished development tasks assigned to specified assignee
        total_count = len(filtered_issues)
        print(f"Total count of finished development tasks assigned to {email}: {total_count}")
else:
    print(f"Failed to retrieve data. Status code: {response.status_code}")

