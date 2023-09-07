#
# Copyright (c) 2023 Oracle, Inc.
# Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl.
#

import oci
from library.createPipeline import CreatePipeline
from library.nodeBuild import Node
from library.parameterBuild import ParameterBuild

from oci.data_integration.data_integration_client import DataIntegrationClient
from oci.data_integration.models.create_pipeline_details import CreatePipelineDetails
from oci.data_integration.models.data_format import DataFormat
from oci.data_integration.models.csv_format_attribute import CsvFormatAttribute
from oci.data_integration.models.compression import Compression



# Enter the values of your configuration as below
#
# workspace_id = '1234'
# service_endpoint="https://dataintegration.us-phoenix-1.oci.oraclecloud.com"
# config = oci.config.from_file('~/.oci/config', 'DEFAULT')
# df_name="MyNewPipeline4"
# df_identifier="MYNEWPIPELINE4"
# folder_id="54949167-04e3-..."
# taskKey="db952c11-c9d7-4fb3-..."
# applicationKey= "a850e495-4626-..."
# connectionKey="378d79d7-a88d-...."

def createPipeline(dip, df_name):
  createPipeline = CreatePipeline(df_name,df_identifier,folder_id)

  #Define a filter parameter with a condition
  filterParam=ParameterBuild(name="FILTER_PARAM")
  filterParam.filterCondition("1=1")
  createPipeline.parameter(filterParam)

  #Define an entity parameter
  entityParam=ParameterBuild(name="ENTITY_PARAM")
  df=DataFormat(type=DataFormat.TYPE_CSV,format_attribute=CsvFormatAttribute(encoding="UTF-8",escape_character="\\",delimiter=",",quote_character="\"",has_header=True,timestamp_format="yyyy-MM-dd HH:mm:ss.SSS"),compression_config=Compression(codec=Compression.CODEC_NONE))
  entityParam.entityWithFormat(connectionKey,"disdemodatax","sanity.csv","FILE_ENTITY", df)
  createPipeline.parameter(entityParam)

  start = Node(name="START1",identifier="START1",type="Start")
  start.toObject("TASK1","INPUT1")
  start.toObject("TASK2","INPUT1")

  task1 = Node(name="TASK1",identifier="TASK1",type="IntegrationTask")
  task1.task("INTEGRATION_TASK", workspace_id, applicationKey, taskKey )
  task1.fromObject("START1","OUTPUT1")
  task1.toObject("MERGE1","INPUT1")
  #Reference a pipeline parameter for the task's input
  task1.parameterRef("INPUT_DATA","ENTITY_PARAM")

  #Define a parameter for the entity as a value
  pv=ParameterBuild(name="INPUT_DATA")
  df=DataFormat(type=DataFormat.TYPE_CSV,format_attribute=CsvFormatAttribute(encoding="UTF-8",escape_character="\\",delimiter=",",quote_character="\"",has_header=True,timestamp_format="yyyy-MM-dd HH:mm:ss.SSS"),compression_config=Compression(codec=Compression.CODEC_NONE))
  pv.entityWithFormat(connectionKey,"disdemodatax","sanity.csv","FILE_ENTITY", df)
  task2 = Node(name="TASK2",identifier="TASK2",type="IntegrationTask")
  task2.parameterValue(pv)

  task2.task("INTEGRATION_TASK", workspace_id, applicationKey, taskKey )
  task2.fromObject("START1","OUTPUT1")
  task2.toObject("MERGE1","INPUT2")

  mrge = Node(name="MERGE1",identifier="MERGE1",type="Merge")
  mrge.fromObject("TASK1","OUTPUT1")
  mrge.fromObject("TASK2","OUTPUT1")
  mrge.toObject("END1","INPUT1")

  end = Node(name="END1",identifier="END1",type="End")
  end.fromObject("MERGE1","OUTPUT1")
  createPipeline.nodes([start,task1,task2,mrge,end])
  createPipelineDetails=createPipeline.build()
  r = None
  try:
    r=createPipeline.create_pipeline(dip, workspace_id, df_name, df_identifier, folder_id, createPipelineDetails)
    print(r.data)
  except:
    print("Complete")
  return r


def main():
  dip=None
  if service_endpoint is None:
    dip = DataIntegrationClient(config)
  else:
    dip = DataIntegrationClient(config,service_endpoint=service_endpoint)

  createPipelineDetails = createPipeline(dip, df_name)

main()