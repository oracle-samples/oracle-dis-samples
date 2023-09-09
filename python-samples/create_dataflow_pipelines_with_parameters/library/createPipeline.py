#!/usr/bin/env python3

# Copyright © 2023, Oracle and/or its affiliates. 
# The Universal Permissive License (UPL), Version 1.0 as shown at https://oss.oracle.com/licenses/upl.

from oci.data_integration.models.create_pipeline_details import CreatePipelineDetails
from oci.data_integration.models.registry_metadata import RegistryMetadata

import uuid


def get_uuid():
    return str(uuid.uuid4())


"""
Helper class to build CreatePipelineDetails payloads for OCI Data Integration.
"""


class CreatePipeline:
    def __init__(self, name, identifier, folder):
        self.name = name
        self.identifier = identifier
        self.folder = folder
        self.flowNodes = []
        self.parameters = []

    def node(self, aNode):
        self.flowNodes.append(aNode.build())

    def nodes(self, allNodes):
        for n in allNodes:
            self.flowNodes.append(n.build())

    def parameter(self, aParameter):
        self.parameters.append(aParameter.build())

    def build(self):
        pipeline_id = get_uuid()
        registry_metadata = RegistryMetadata(aggregator_key=self.folder)
        create_details = CreatePipelineDetails(key=pipeline_id,
                                               name=self.name,
                                               identifier=self.identifier,
                                               registry_metadata=registry_metadata,
                                               nodes=self.flowNodes,
                                               parameters=self.parameters
                                               )
        return create_details

    def create_pipeline(self, di_client, workspace, df_name, df_identifier, folder_id, create_df_details):
        create_response = di_client.create_pipeline(
            workspace, create_df_details)
        return create_response
