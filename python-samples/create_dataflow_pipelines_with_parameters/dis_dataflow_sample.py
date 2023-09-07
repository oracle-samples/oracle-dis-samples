#!/usr/bin/env python3

# Copyright © 2023, Oracle and/or its affiliates. 
# The Universal Permissive License (UPL), Version 1.0 as shown at https://oss.oracle.com/licenses/upl.

import oci
import getopt, sys

from library.createDataFlow import CreateDataflow
from library.nodeBuild import Node
from library.parameterBuild import ParameterBuild

from oci.data_integration.data_integration_client import DataIntegrationClient
from oci.data_integration.models.create_data_flow_details import CreateDataFlowDetails
from oci.data_integration.models.data_format import DataFormat
from oci.data_integration.models.compression import Compression
from oci.data_integration.models.csv_format_attribute import CsvFormatAttribute

config = oci.config.from_file(profile_name="DEFAULT")
data_integration_client = DataIntegrationClient(config)

def createDataflow(dip, df_name, df_identifier, workspace_id, inputfile, outputfile, source_data_asset_id, source_conn_id,
                   target_data_asset_id, target_conn_id, folder_id, schema):

  cd = CreateDataflow(df_name,df_identifier,folder_id)

  src = Node(name="SOURCE1",identifier="SOURCE1",type="Source")
  src.toObject("FILTER1","INPUT1")
  src.dataAsset("ORACLE_OBJECT_STORAGE_DATA_ASSET", source_data_asset_id)
  src.connection("ORACLE_OBJECT_STORAGE_CONNECTION", source_conn_id)
  src.schema(schema)
  src.entity("FILE_ENTITY", inputfile)
  src.operatorProperty( "dataFormat",DataFormat(type=DataFormat.TYPE_CSV,format_attribute=CsvFormatAttribute(encoding="UTF-8",escape_character="\\",delimiter=",",quote_character="\"",has_header=True,timestamp_format="yyyy-MM-dd HH:mm:ss.SSS"),compression_config=Compression(codec=Compression.CODEC_NONE)))

  filter = Node(name="FILTER1",identifier="FILTER1",type="Filter")
  filter.fromObject("SOURCE1","OUTPUT1")
  filter.toObject("TARGET1","INPUT1")
  filter.operatorProperty( "filterCondition","INFIELD1.SOURCE1.PO_DISTRIBUTION_ID IS NOT NULL")

  tgt = Node(name="TARGET1",identifier="TARGET1",type="Target")
  tgt.fromObject("FILTER1","OUTPUT1")
  tgt.dataAsset("ORACLE_OBJECT_STORAGE_DATA_ASSET", target_data_asset_id)
  tgt.connection("ORACLE_OBJECT_STORAGE_CONNECTION", target_conn_id)
  tgt.schema(schema)
  tgt.entity("FILE_ENTITY", outputfile)
  tgt.operatorProperty( "dataFormat",DataFormat(type=DataFormat.TYPE_CSV,format_attribute=CsvFormatAttribute(encoding="UTF-8",escape_character="\\",delimiter=",",quote_character="\"",has_header=True,timestamp_format="yyyy-MM-dd HH:mm:ss.SSS"),compression_config=Compression(codec=Compression.CODEC_NONE)))
  tgt.operatorProperty( "createNewEntity",True)

  cd.nodes([src,filter,tgt])
#  print("Nodes = " + str(cd.nodes))

  createDataFlowDetails=cd.build()
#  print("DF Details = " + str(createDataFlowDetails))

  r=cd.create_dataflow(dip, workspace_id, df_name, df_identifier, folder_id, createDataFlowDetails)

  return r

def main():

  argumentList = sys.argv[1:]
  options = "h:w:i:o:df:id:s:t:sc:tc;f;sh"
  long_options = ["Help", "workspace=", "inputfile=", "outputfile=", "df_name=", "df_identifier=", "source_da=", "target_da=", "source_conn=", "target_conn=", "folder_id=", "schema="]
  df_name = ""
  df_identifier = ""
  workspace_id = ""
  inputfile = ""
  outputfile = ""
  source_data_asset_id = ""
  source_conn_id = ""
  target_data_asset_id = ""
  target_conn_id = ""
  folder_id = ""
  schema = ""

  try:
    arguments, values = getopt.getopt(argumentList, options, long_options)
    for currentArgument, currentValue in arguments:
      if currentArgument in ("-h", "--Help"):
        print("--workspace workspace_id --inputfile filename --outputfile outputfilename --df_name dataflow_name --df_identifier df_identifier --source_da source_data_asset_id \
        --target_da target_da_id --source_conn source_connection_id --target_conn target_conn_id --folder folder_id --schema schema" )
      elif currentArgument in ("-w", "--workspace"):
        workspace_id = currentValue
      elif currentArgument in ("-i", "--inputfile"):
        inputfile = currentValue
      elif currentArgument in ("-o", "--outputfile"):
        outputfile = currentValue
      elif currentArgument in ("-df", "--dataflow_name"):
        df_name = currentValue
      elif currentArgument in ("-id", "--df_identifier"):
        df_identifier = currentValue
      elif currentArgument in ("-s", "--source_da"):
        source_data_asset_id = currentValue
        print("Source Asset ID = " + source_data_asset_id)
      elif currentArgument in ("-t", "--target_da"):
        target_data_asset_id = currentValue
      elif currentArgument in ("-sc", "--source_conn"):
        source_conn_id = currentValue
        print("Source conn ID = " + source_conn_id)
      elif currentArgument in ("-tc", "--target_conn"):
        target_conn_id = currentValue
      elif currentArgument in ("-f", "--folder"):
        folder_id = currentValue
      elif currentArgument in ("-sh", "--schema"):
        schema = currentValue
  except getopt.error as err:
    print(str(err))

  dip = DataIntegrationClient(config)

  createDataFlowDetails = createDataflow(dip, df_name, df_identifier, workspace_id, inputfile, outputfile, source_data_asset_id, source_conn_id,
                                         target_data_asset_id, target_conn_id, folder_id, schema)

main()
