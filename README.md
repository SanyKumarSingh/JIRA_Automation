#Automation Jobs Scripts

# copy_gz_job.sh
Shell Script to migrate the files from Parser NFS Processed directory .snapshot to the OCI Object Storage.

Copy the File from Local to UnixBox
scp C:\Users\a5143522\CodeBase\PythonJobs\copy_gz_job.sh ocradmin@oeforapars001d.adwin.renesas.com:/localdisk/ocradmin/bin
scp /localdisk/ocradmin/bin/copy_gz_job.sh ocradmin@oeforapars003p.adwin.renesas.com:/localdisk/ocradmin/bin

Convert the file from Windows to Unix Format
[ocradmin@oeforapars001d bin]$ dos2unix /localdisk/ocradmin/bin/copy_gz_job.sh
dos2unix: converting file /localdisk/ocradmin/bin/copy_gz_job.sh to Unix format...

Execution/Run Shell Script command  - [ocradmin@oeforapars001d bin]$ sh /localdisk/ocradmin/bin/copy_gz_job.sh

Execution Shell via nohup to open a new session to run in the background
[ocradmin@oeforapars001d bin]$ nohup /localdisk/ocradmin/bin/copy_gz_job.sh  > outpufile_copy_job 2>&1 &
[1] 1997781
-rw-r--r--.  1 ocradmin dlgusers   22 Apr 12 14:34 outpufile_copy_job
[1]+  Done                    nohup /localdisk/ocradmin/bin/copy_gz_job.sh > outpufile_copy_job 2>&1
[ocradmin@oeforapars001d bin]$ tail -1000 outpufile_copy_job
nohup: ignoring input

# jira_task.py
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
