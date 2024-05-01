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
import requests     # requests library to interact with the Jira REST API
import json         # json module
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

# Construct the assignees' emails
assignees_emails = ['Sany.Singh@diasemi.com', 'Paulo.Safaro@diasemi.com']  # Update with actual email addresses
assignees_emails_str = ', '.join(f'"{email}"' for email in assignees_emails)

# Construct JQL query to find finished development tasks for assignees' emails
JQL_QUERY = f'project = "GYM" AND status = Done AND issuetype = "Sub-task" AND assignee in ({assignees_emails_str}) AND resolutiondate >= {seven_days_ago_str}'

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
    
    # Filter issues based on assignee's email
    filtered_issues = [issue for issue in data['issues'] if issue['fields']['assignee']['emailAddress'] == 'Sany.Singh@diasemi.com']
    
    # Print count of finished development tasks assigned to specified assignees
    total_count = len(filtered_issues)
    print(f"Total count of finished development tasks assigned to Sany.Singh@diasemi.com: {total_count}")
    
    # Filter issues based on assignee's email
    filtered_issues = [issue for issue in data['issues'] if issue['fields']['assignee']['emailAddress'] == 'Paulo.Safaro@diasemi.com']
    
    # Print count of finished development tasks assigned to specified assignees
    total_count = len(filtered_issues)
    print(f"Total count of finished development tasks assigned to Paulo.Safaro@diasemi.com: {total_count}")
    
else:
    print(f"Failed to retrieve data. Status code: {response.status_code}")

