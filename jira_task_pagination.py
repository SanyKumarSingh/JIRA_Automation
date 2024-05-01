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
    'jql': JQL_QUERY,
    'maxResults': 50,  # Fetch 50 results per page
    'startAt': 0       # Start at the first page
}

# Set flag to determine whether to use pagination to fetch all records from JIRA 
# or fine with only max 50 records as per JIRA limit
# values are True or False
use_pagination = False

# Initialize list to store all issues
all_issues = []

# Make initial API call to get total number of issues
response = requests.get(JIRA_URL, params=params, auth=auth_header, verify=False)

# Check if the request was successful
if response.status_code == 200:
    # Parse JSON response
    data = response.json()
    
    # Get total number of issues
    total_issues = data['total']
    print(f"Total count of finished development tasks: {total_issues}")
    
    # Check if pagination is enabled and use it if necessary
    if use_pagination:
        # Fetch all issues using pagination
        while len(all_issues) < total_issues:
            # Make API call with updated startAt parameter
            response = requests.get(JIRA_URL, params=params, auth=auth_header, verify=False)
            
            # Parse JSON response and append issues to all_issues
            data = response.json()
            all_issues.extend(data.get('issues', []))
            
            # Update startAt parameter for next page
            params['startAt'] += params['maxResults']
    else:
        # Fetch all issues without pagination
        all_issues = data.get('issues', [])
    
    # Check if all_issues is None or empty
    if all_issues is None or len(all_issues) == 0:
        print("No issues found.")
    else:
        # Save JSON response containing all issues to a file
        with open('all_issues.json', 'w') as f:
            f.write(json.dumps({'issues': all_issues}))
        print("JSON data for all issues saved to 'all_issues.json' file.")
        
        # Check if all_issues is not None before filtering ssingh_issues
        if all_issues:
            # Filter issues assigned to user "ssingh"
            ssingh_issues = [issue for issue in all_issues if issue.get('fields', {}).get('assignee', {}).get('key') == 'ssingh']
            
            # Print count of finished development tasks assigned to "ssingh"
            total_count = len(ssingh_issues)
            print(f"Total count of finished development tasks assigned to 'ssingh': {total_count}")
            
            # Save JSON response containing only "ssingh" issues to a file
            with open('ssingh_issues.json', 'w') as f:
                f.write(json.dumps({'issues': ssingh_issues}))
            print("JSON data for 'ssingh' issues saved to 'ssingh_issues.json' file.")
else:
    print(f"Failed to retrieve data. Status code: {response.status_code}")
