#Automation Jobs Scripts

# email_user_jira_task.py
Python Script to call the Atlasian JIRA Rest API. Detailed documentation - https://confluence.renesas.com/display/GMANUF/JIRA+Automation

As part of our DevOps initiative - https://confluence.renesas.com/display/GMANUF/DevOps we are working on the Rest API to fetch the list of completed task in a Sprint/Week to get a report per week.

1)	Count of production support tickets closed (iGate/GYM/Midas/Spotfire)
2)	Count of development tasks finished, in Jira or otherwise
3)	List of open projects you are working on
4)	List of significant tasks closed on open projects or projects closed during previous week (for example, completed a new parser, completed a new service, etc.)


C:\Users\a5143522\CodeBase\automation_jobs\automation_jobs>python jira_task.py

curl -u username:password -X GET --insecure "https://jira.global.renesas.com/rest/api/2/myself"
curl -u jiraadm_internal:SVY7sj37ssW9 -X GET --insecure "https://jira.global.renesas.com/rest/api/2/myself"

curl -u username:password -X GET --insecure -H "Content-Type: application/json" "https://jira.global.renesas.com/rest/api/2/search?jql=project=%22GYM%22%20AND%20status=Done%20AND%20issuetype=%22Sub-task%22"
curl -u jiraadm_internal:SVY7sj37ssW9 -X GET --insecure -H "Content-Type: application/json" "https://jira.global.renesas.com/rest/api/2/search?jql=project=%22GYM%22%20AND%20status=Done%20AND%20issuetype=%22Sub-task%22"



Test and use the Rest API provided by Jira - Atlassian tools to automate the manual reporting tasks.

First do the Python Setup following the document - Python Setup

Example Jira Rest API  

To Fetch user profile details - https://jira.global.renesas.com/rest/api/2/myself


C:\Users\a5143522\CodeBase\PythonJobs> curl -u username:password -X GET "https://jira.global.renesas.com/rest/api/2/myself"
C:\Users\a5143522\CodeBase\PythonJobs> curl -u username:password -X GET --insecure "https://jira.global.renesas.com/rest/api/2/myself"

## Use the username and password that has access to the Jira Rest Api.

2. To Fetch the task completion details - https://jira.global.renesas.com/rest/api/2/search

C:\Users\a5143522\CodeBase\PythonJobs> curl -u username:password -X GET -H "Content-Type: application/json" "https://jira.global.renesas.com/rest/api/2/search?jql=project=%22GYM%22%20AND%20status=Done%20AND%20issuetype=%22Sub-task%22"



C:\Users\a5143522\CodeBase\automation_jobs\automation_jobs>python jira_task.py
C:\Users\a5143522\AppData\Local\Programs\Python\Python312\Lib\site-packages\urllib3\connectionpool.py:1103: InsecureRequestWarning: Unverified HTTPS request is being made to host 'jira.global.renesas.com'. Adding certificate verification is strongly advised. See: https://urllib3.readthedocs.io/en/latest/advanced-usage.html#tls-warnings
  warnings.warn(
Total count of finished development tasks: 216
JSON data saved to 'jira_data.json' file.
Total count of finished development tasks assigned to 'ssingh': 49
JSON data for 'ssingh' issues saved to 'ssingh_issues.json' file.

C:\Users\a5143522\CodeBase\automation_jobs\automation_jobs>



 Script Execution steps -
 C:\Users\a5143522\CodeBase\automation_jobs\automation_jobs>python email_user_jira_task.py
 Enter assignees' emails separated by commas: # Sany.Singh@diasemi.com,Paulo.Safaro@diasemi.com,chris.baptist.eb@renesas.com,ahamad.shaik.vf@renesas.com,Tasos.Dekazos@diasemi.com
 C:\Users\a5143522\AppData\Local\Programs\Python\Python312\Lib\site-packages\urllib3\connectionpool.py:1103: InsecureRequestWarning: Unverified HTTPS request is being made to host 'jira.global.renesas.com'. Adding certificate verification is strongly advised. See: https://urllib3.readthedocs.io/en/latest/advanced-usage.html#tls-warnings
  warnings.warn(
 Report sent successfully via email.
 C:\Users\a5143522\CodeBase\automation_jobs\automation_jobs>



We have automated the weekly task reporting using python script for all the Sub-Task that have been completed in the week by our team members Sany.Singh@diasemi.com,Paulo.Safaro@diasemi.com,chris.baptist.eb@renesas.com,ahamad.shaik.vf@renesas.com,Tasos.Dekazos@diasemi.com



The script is here - https://bitbucket.global.renesas.com/users/ssingh/repos/automation_jobs/browse/email_user_jira_task.py

We need to discuss in our team if we can all update JIRA tasks so this automated report can capture data accurately. In that case individual manual weekly reporting and the effort of consolidating report could be saved. 

This is not a scheduled job yet, we can discuss if we would like to utilize this automation or not in the team meeting.