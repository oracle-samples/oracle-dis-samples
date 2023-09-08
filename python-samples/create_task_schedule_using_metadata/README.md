# Introduction

This script can create [schedules](https://docs.oracle.com/en-us/iaas/data-integration/using/create-schedule-cron.htm#create-cron-schedule) in OCI Data Integration from a tab delimited file or [task schedules](https://docs.oracle.com/en-us/iaas/data-integration/using/create-task-schedule.htm). The workspace ocid and application key are passed as parameters. The schedules and task schedules are created in this application/workspace and the referenced tasks and schedules are within it. This depends on the OCI Python SDK which is available in the [OCI Console Cloud Shell](https://docs.oracle.com/en-us/iaas/Content/API/Concepts/cloudshellintro.htm) preconfigured or can be installed locally (see [here](https://docs.oracle.com/en-us/iaas/Content/API/SDKDocs/pythonsdk.htm) for details).

Save the Python file create_task_schedules.py into your client (easiest is Cloud Shell), then save same tsv file(s) for your schedules or task schedules. If you have the OCI Python SDK installed which is already installed in CloudShell, get your workspace OCID and application key and you can run the script.

# Script Parameters

Script parameters;

* --workspace workspace ocid is mandatory.
* --application application key is mandatory.
* --inputfile tab delimited file for schedules or task schedules is mandatory.
* --type SCHEDULES OR TASK_SCHEDULES, by default TASK_SCHEDULES are created, this parameter is optional.

## Example - Create task schedules

```python3 create_task_schedules.py --workspace workspace_ocid --application application_key --inputfile tasks.tsv```

## Example Create schedules

```python3 create_task_schedules.py --workspace workspace_ocid --application application_key --inputfile schedules.tsv -t SCHEDULES```

# Schedule File

The columns should be tab separated and include;
* SCHEDULE_NAME eg. My Schedule
* CRON_EXPRESSION eg */30 * * * *
* TIMEZONE eg PST
* ENABLED eg. True

# Task Schedule File

The columns should be tab separated and include;

* SCHEDULE - name for the schedule to use
* NAME - name for the task schedule
* ENABLED - True or False to enable the task schedule
* TASK - task name that resides in the application that is passed to script

## Author
David Allan - Consultant Principal Architect 

david.allan@oracle.com




