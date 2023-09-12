#!/usr/bin/env python3

# Copyright © 2023, Oracle and/or its affiliates. 
# The Universal Permissive License (UPL)
# Version 1.0 as shown at https://oss.oracle.com/licenses/upl.

import oci
import argparse
from library.createDataFlow import CreateDataflow
from library.nodeBuild import Node

from oci.data_integration.data_integration_client import DataIntegrationClient
from oci.data_integration.models.data_format import DataFormat
from oci.data_integration.models.compression import Compression
from oci.data_integration.models.csv_format_attribute import CsvFormatAttribute


def createDataflow(dip, df_name, df_identifier,
                   workspace_id, inputfile, outputfile,
                   source_data_asset_id, source_conn_id,
                   target_data_asset_id, target_conn_id,
                   folder_id, schema):

    cd = CreateDataflow(df_name, df_identifier, folder_id)

    src = Node(name="SOURCE1", identifier="SOURCE1", type="Source")
    src.toObject("FILTER1", "INPUT1")
    src.dataAsset("ORACLE_OBJECT_STORAGE_DATA_ASSET", source_data_asset_id)
    src.connection("ORACLE_OBJECT_STORAGE_CONNECTION", source_conn_id)
    src.schema(schema)
    src.entity("FILE_ENTITY", inputfile)
    src.operatorProperty("dataFormat",
                         DataFormat(
                             type=DataFormat.TYPE_CSV,
                             format_attribute=CsvFormatAttribute(
                                 encoding="UTF-8",
                                 escape_character="\\",
                                 delimiter=",",
                                 quote_character="\"",
                                 has_header=True,
                                 timestamp_format="yyyy-MM-dd HH:mm:ss.SSS"),
                             compression_config=Compression(
                                 codec=Compression.CODEC_NONE)))

    filter = Node(name="FILTER1", identifier="FILTER1", type="Filter")
    filter.fromObject("SOURCE1", "OUTPUT1")
    filter.toObject("TARGET1", "INPUT1")
    filter.operatorProperty(
        "filterCondition", "INFIELD1.SOURCE1.PO_DISTRIBUTION_ID IS NOT NULL")

    tgt = Node(name="TARGET1", identifier="TARGET1", type="Target")
    tgt.fromObject("FILTER1", "OUTPUT1")
    tgt.dataAsset("ORACLE_OBJECT_STORAGE_DATA_ASSET", target_data_asset_id)
    tgt.connection("ORACLE_OBJECT_STORAGE_CONNECTION", target_conn_id)
    tgt.schema(schema)
    tgt.entity("FILE_ENTITY", outputfile)
    tgt.operatorProperty("dataFormat",
                         DataFormat(
                             type=DataFormat.TYPE_CSV,
                             format_attribute=CsvFormatAttribute(
                                 encoding="UTF-8",
                                 escape_character="\\",
                                 delimiter=",",
                                 quote_character="\"",
                                 has_header=True,
                                 timestamp_format="yyyy-MM-dd HH:mm:ss.SSS"),
                             compression_config=Compression(
                                 codec=Compression.CODEC_NONE)))
    tgt.operatorProperty("createNewEntity", True)

    cd.nodes([src, filter, tgt])
    r = cd.create_dataflow(dip,
                           workspace_id,
                           df_name,
                           df_identifier,
                           folder_id,
                           cd.build())

    return r


def main(args, client):

    createDataFlowDetails = createDataflow(client,
                                           args.dataflow_name,
                                           args.df_identifier,
                                           args.workspace,
                                           args.input_file,
                                           args.output_file,
                                           args.source_da,
                                           args.source_conn,
                                           args.target_da,
                                           args.target_conn,
                                           args.folder,
                                           args.schema)

    if createDataFlowDetails.status != 200:
        print("Failed to create Data Flow")
        print(createDataFlowDetails.data)
        exit(1)
    else:
        print("Data Flow ID:" + createDataFlowDetails.data.id)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-w', '--workspace',
                        help='DIS workspace OCID; ocid1.disworkspace.oc1...')
    parser.add_argument('-i', '--input_file',
                        default='',
                        help='Input file')
    parser.add_argument('-o', '--output_file',
                        default='',
                        help='Output file')
    parser.add_argument('-df', '--dataflow_name',
                        default='',
                        help='dataflow name')
    parser.add_argument('-id', '--df_identifier',
                        default='',
                        help='dataflow ID')
    parser.add_argument('-s', '--source_da',
                        default='',
                        help='Data Source Data Asset Key')
    parser.add_argument('-sc', '--source_conn',
                        default='',
                        help='Data Source connection key')
    parser.add_argument('-t', '--target_da',
                        default='',
                        help='Data Target Data Asset key')
    parser.add_argument('-tc', '--target_conn',
                        default='',
                        help='Data Target connection key')
    parser.add_argument('-f', '--folder',
                        default='',
                        help='Folder key')
    parser.add_argument('-sh', '--schema',
                        default='',
                        help='Data Scema')
    parser.add_argument('-p', '--profile',
                        default='DEFAULT',
                        help='Profile for ~/.oci/config')

    args = parser.parse_args()
    config = oci.config.from_file(profile_name=args.profile)
    data_integration_client = DataIntegrationClient(config)

    main(args, data_integration_client)

