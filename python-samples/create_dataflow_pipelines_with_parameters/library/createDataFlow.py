#!/usr/bin/env python3

# Copyright © 2023, Oracle and/or its affiliates. 
# The Universal Permissive License (UPL), Version 1.0 as shown at https://oss.oracle.com/licenses/upl.

# Extending CreateDataflow
from oci.data_integration.models.create_data_flow_details import CreateDataFlowDetails
from oci.data_integration.models.registry_metadata import RegistryMetadata
import uuid

def get_uuid():
    return str(uuid.uuid4())

"""
Dataflows have nodes and parameters, they can be added to the flow using node(), nodes() and parameter() methods.
The node object can be built using the Node class and the parameter object can be built using ParameterBuild.
"""
class CreateDataflow:
  def __init__(self,name,identifier,folder):
    self.name = name
    self.identifier = identifier
    self.folder = folder
    self.flowNodes=[]
    self.parameters=[]
  def node(self,aNode):
    self.flowNodes.append(aNode.build())
  def nodes(self,allNodes):
    checkNodes = {}
    for n in allNodes:
      checkNodes[n.name]=True
    for n in allNodes:
      for fob in n.fromObjects:
        if (checkNodes.get(fob.node) is None):
          raise Exception('Node referenced ' + fob.node + ' in from link does not exist ', n.name)
      for tob in n.toObjects:
        if (checkNodes.get(tob.node) is None):
          raise Exception('Node referenced ' + tob.node + ' in to link does not exist ', n.name)

    for n in allNodes:
      self.flowNodes.append(n.build())
  def parameter(self,aParameter):
    self.parameters.append(aParameter.build())
  def build(self):
    pipeline_id = get_uuid()
    registry_metadata=RegistryMetadata(aggregator_key=self.folder)
    create_df_details= CreateDataFlowDetails(key=pipeline_id,
                                 name=self.name,
                                 identifier=self.identifier,
                                 registry_metadata=registry_metadata,
                                 nodes=self.flowNodes,
                                 parameters=self.parameters
                                 )
    return create_df_details

  def create_dataflow(self, di_client, workspace, df_name, df_identifier, folder_id, create_df_details):
    pipeline_id = get_uuid()
    registry_metadata = RegistryMetadata(aggregator_key=folder_id)
    create_response = di_client.create_data_flow(workspace, create_df_details)
    return create_response


