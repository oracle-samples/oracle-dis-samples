#!/usr/bin/env python3

# Copyright © 2023, Oracle and/or its affiliates. 
# The Universal Permissive License (UPL), Version 1.0 as shown at https://oss.oracle.com/licenses/upl.

import getopt
import sys
import oci
import csv
from oci.data_integration.data_integration_client import DataIntegrationClient

config = oci.config.from_file()
data_integration_client = DataIntegrationClient(config)


def create_schedule(data_integration_client, workspace_id, application_key, schedule_name, timezone, cron_expression, daylight_enabled):
    create_schedule_response = data_integration_client.create_schedule(
        workspace_id=workspace_id,
        application_key=application_key,
        create_schedule_details=oci.data_integration.models.CreateScheduleDetails(
            name=schedule_name,
            identifier=schedule_name.upper().replace(" ", "_"),
            timezone=timezone,
            is_daylight_adjustment_enabled=daylight_enabled,
            frequency_details=oci.data_integration.models.CustomFrequencyDetails(
                custom_expression=cron_expression)
        ))
    return create_schedule_response


def create_task_schedule(data_integration_client, workspace_id, application_key, task_key, task_schedule_name, schedule_key, enabled):
    create_task_schedule_response = data_integration_client.create_task_schedule(
        workspace_id=workspace_id,
        application_key=application_key,
        create_task_schedule_details=oci.data_integration.models.CreateTaskScheduleDetails(
            name=task_schedule_name,
            identifier=task_schedule_name.upper().replace(" ", "_"),
            schedule_ref=oci.data_integration.models.Schedule(
                object_status=1, key=schedule_key),
            is_enabled=enabled,
            registry_metadata=oci.data_integration.models.RegistryMetadata(aggregator_key=task_key)))
    return create_task_schedule_response


def get_task_key(data_integration_client, workspace_id, application_key, task_name):
    tsk = data_integration_client.list_published_objects(
        workspace_id=workspace_id,
        application_key=application_key,
        name=task_name
    )
    return tsk.data.items[0]


def get_schedule_key(data_integration_client, workspace_id, application_key, schedule_name):
    sch = data_integration_client.list_schedules(
        workspace_id=workspace_id,
        application_key=application_key,
        name=schedule_name
    )
    return sch.data.items[0]


def create_task_schedules(data_integration_client, filename, workspace_id, application_key):
    with open(filename, newline='') as csvfile:
        taskschreader = csv.reader(csvfile, dialect='excel-tab')
        line = 0
        for row in taskschreader:
            line = line+1
            if (line == 1):
                continue
            schedule_name = row[0]
            task_schedule_name = row[1]
            enabled = row[2]
            task_name = row[3]
            print("Creating task schedule " + task_schedule_name +
                  " for task " + task_name + " using schedule " + schedule_name)
            sch = get_schedule_key(
                data_integration_client, workspace_id, application_key, schedule_name)
            tsk = get_task_key(data_integration_client,
                               workspace_id, application_key, task_name)
            tasksch = create_task_schedule(data_integration_client, workspace_id,
                                           application_key, tsk.key, task_schedule_name, sch.key, bool(enabled))
            print(tasksch.data.key)


def create_schedules(data_integration_client, filename, workspace_id, application_key):
    with open(filename, newline='') as csvfile:
        schedulereader = csv.reader(csvfile, dialect='excel-tab')
        line = 0
        for row in schedulereader:
            line = line+1
            if (line == 1):
                continue
            schedule_name = row[0]
            cron_expression = row[1]
            timezone = row[2]
            enabled = row[3]
            print("Creating schedule " + schedule_name + " using cron expression " +
                  cron_expression + " in timezone " + timezone)
            sch = create_schedule(data_integration_client, workspace_id, application_key,
                                  schedule_name, timezone, cron_expression, bool(enabled))
            print(sch.data.key)


argumentList = sys.argv[1:]
options = "h:w:a:i:t:"
long_options = ["Help", "workspace=", "application=", "inputfile="]
workspace_id = "TBD"
application_key = "TBD"
object_type = "TASK_SCHEDULE"

try:
    arguments, values = getopt.getopt(argumentList, options, long_options)
    for currentArgument, currentValue in arguments:
        if currentArgument in ("-h", "--Help"):
            print(
                "--workspace workspace_id --application application_key -inputfile filename")
        elif currentArgument in ("-w", "--workspace"):
            workspace_id = currentValue
        elif currentArgument in ("-a", "--application"):
            application_key = currentValue
        elif currentArgument in ("-i", "--inputfile"):
            filename = currentValue
        elif currentArgument in ("-t", "--type"):
            object_type = currentValue
except getopt.error as err:
    print(str(err))

if (object_type == "TASK_SCHEDULE"):
    create_task_schedules(data_integration_client,
                          filename, workspace_id, application_key)
else:
    create_schedules(data_integration_client, filename,
                     workspace_id, application_key)
