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

# Define Jira credentials and base URL
USERNAME = 'jiraadm_internal'
PASSWORD = 'SVY7sj37ssW9'
JIRA_URL = 'https://jira.global.renesas.com/rest/api/2/search'

# Construct JQL query to find finished development tasks
JQL_QUERY = 'project = "GYM" AND status = Done AND issuetype = "Sub-task"'

# Construct authentication header
auth_header = (USERNAME, PASSWORD)

# Define parameters for the API call
params = {
    'jql': JQL_QUERY
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
    
    # Filter issues assigned to user "ssingh"
    ssingh_issues = [issue for issue in data['issues'] if issue['fields']['assignee']['key'] == 'ssingh']
    
    # Print count of finished development tasks assigned to "ssingh"
    total_count = len(ssingh_issues)
    print(f"Total count of finished development tasks assigned to 'ssingh': {total_count}")
    
    # Save JSON response containing only "ssingh" issues to a file
    with open('ssingh_issues.json', 'w') as f:
        f.write(json.dumps({'issues': ssingh_issues}))
    print("JSON data for 'ssingh' issues saved to 'ssingh_issues.json' file.")
else:
    print(f"Failed to retrieve data. Status code: {response.status_code}")

