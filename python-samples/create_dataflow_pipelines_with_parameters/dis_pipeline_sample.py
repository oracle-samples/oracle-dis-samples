#!/usr/bin/env python3

#
# Copyright (c) 2023 Oracle, Inc.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl.
#
import oci
import argparse
import getopt

from library.createPipeline import CreatePipeline
from library.nodeBuild import Node
from library.parameterBuild import ParameterBuild

from oci.data_integration.data_integration_client import DataIntegrationClient
from oci.data_integration.models.data_format import DataFormat
from oci.data_integration.models.csv_format_attribute import CsvFormatAttribute
from oci.data_integration.models.compression import Compression


def createPipeline(dip, df_name, df_identifier, workspace, connection_key,
                   application_key, task_key, folder_id):
    createPipeline = CreatePipeline(df_name, df_identifier, workspace,
                                    connection_key, application_key, task_key, folder_id)

    # Define a filter parameter with a condition
    filterParam = ParameterBuild(name="FILTER_PARAM")
    filterParam.filterCondition("1=1")
    createPipeline.parameter(filterParam)

    # Define an entity parameter
    entityParam = ParameterBuild(name="ENTITY_PARAM")
    df = DataFormat(type=DataFormat.TYPE_CSV, format_attribute=CsvFormatAttribute(encoding="UTF-8", escape_character="\\", delimiter=",",
                    quote_character="\"", has_header=True, timestamp_format="yyyy-MM-dd HH:mm:ss.SSS"), compression_config=Compression(codec=Compression.CODEC_NONE))
    entityParam.entityWithFormat(
        connection_key, "disdemodatax", "sanity.csv", "FILE_ENTITY", df)
    createPipeline.parameter(entityParam)

    start = Node(name="START1", identifier="START1", type="Start")
    start.toObject("TASK1", "INPUT1")
    start.toObject("TASK2", "INPUT1")

    task1 = Node(name="TASK1", identifier="TASK1", type="IntegrationTask")
    task1.task("INTEGRATION_TASK", workspace, application_key, task_key)
    task1.fromObject("START1", "OUTPUT1")
    task1.toObject("MERGE1", "INPUT1")
    # Reference a pipeline parameter for the task's input
    task1.parameterRef("INPUT_DATA", "ENTITY_PARAM")

    # Define a parameter for the entity as a value
    pv = ParameterBuild(name="INPUT_DATA")
    df = DataFormat(type=DataFormat.TYPE_CSV, format_attribute=CsvFormatAttribute(encoding="UTF-8", escape_character="\\", delimiter=",",
                    quote_character="\"", has_header=True, timestamp_format="yyyy-MM-dd HH:mm:ss.SSS"), compression_config=Compression(codec=Compression.CODEC_NONE))
    pv.entityWithFormat(connection_key, "disdemodatax",
                        "sanity.csv", "FILE_ENTITY", df)
    task2 = Node(name="TASK2", identifier="TASK2", type="IntegrationTask")
    task2.parameterValue(pv)

    task2.task("INTEGRATION_TASK", workspace, application_key, task_key)
    task2.fromObject("START1", "OUTPUT1")
    task2.toObject("MERGE1", "INPUT2")

    mrge = Node(name="MERGE1", identifier="MERGE1", type="Merge")
    mrge.fromObject("TASK1", "OUTPUT1")
    mrge.fromObject("TASK2", "OUTPUT1")
    mrge.toObject("END1", "INPUT1")

    end = Node(name="END1", identifier="END1", type="End")
    end.fromObject("MERGE1", "OUTPUT1")
    createPipeline.nodes([start, task1, task2, mrge, end])
    createPipelineDetails = createPipeline.build()
    r = None
    try:
        r = createPipeline.create_pipeline(
            dip, workspace, df_name, df_identifier, folder_id, createPipelineDetails)
        print(r.data)
    except getopt.error as err:
        print(str(err))
    return r


def main(args, client):

    createPipelineDetails = createPipeline(client,
                                           args.pipeline_name,
                                           args.pipeline_identifier,
                                           args.workspace,
                                           args.connection_key,
                                           args.application_key,
                                           args.task_key,
                                           args.folder,
                                           args.profile)

    if createPipelineDetails.status != 200:
        print("Failed to create Data Flow")
        print(createPipelineDetails.data)
        exit(1)
    else:
        print("Data Flow ID:" + createPipelineDetails.data.id)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-w', '--workspace',
                        help='DIS workspace OCID; ocid1.disworkspace.oc1...')
    parser.add_argument('-pn', '--pipeline_name',
                        default='',
                        help='pipeline name')
    parser.add_argument('-id', '--pipeline_identifier',
                        default='',
                        help='Pipeline ID')
    parser.add_argument('-sc', '--connection_key',
                        default='',
                        help='Connection key')
    parser.add_argument('-a', '--application_key',
                        default='',
                        help='Application key')
    parser.add_argument('-t', '--task_key',
                        default='',
                        help='Task key')
    parser.add_argument('-f', '--folder',
                        default='',
                        help='Folder for the pipeline')
    parser.add_argument('-p', '--profile',
                        default='DEFAULT',
                        help='Profile for ~/.oci/config')

    args = parser.parse_args()
    config = oci.config.from_file(profile_name=args.profile)
    data_integration_client = DataIntegrationClient(config)

    main(args, data_integration_client)
