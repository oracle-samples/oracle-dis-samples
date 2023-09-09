#!/usr/bin/env python3

# Copyright © 2023, Oracle and/or its affiliates. 
# The Universal Permissive License (UPL), Version 1.0 as shown at https://oss.oracle.com/licenses/upl.

from oci.data_integration.models.parameter import Parameter
from oci.data_integration.models.shape import Shape
from oci.data_integration.models.data_entity_from_file import DataEntityFromFile
from oci.data_integration.models.data_entity_from_table import DataEntityFromTable
from oci.data_integration.models.composite_type import CompositeType
from oci.data_integration.models.parent_reference import ParentReference
from oci.data_integration.models.java_type import JavaType
from oci.data_integration.models.schema import Schema
from oci.data_integration.models.enriched_entity import EnrichedEntity

import uuid


def get_uuid():
    return str(uuid.uuid4())


idCache = {}


def getUuid(reference):
    theUUID = idCache.get(reference)
    if (theUUID is None):
        uuid = get_uuid()
        idCache[reference] = uuid
        return uuid
    return theUUID


class ParameterBuild:
    def __init__(self, name):
        self.name = name
        self.connectionKey = None
        self.schema = None
        self.entityName = None
        self.entityType = None
        self.dataFormat = None
        self.dataAssetKey = None
        self.stringValue = None

    def dataAsset(self, dataAssetKey):
        self.dataAssetKey = dataAssetKey

    def connection(self, key):
        self.connectionKey = key

    def schema(self, conKey, key):
        self.connectionKey = conKey
        self.schema = key

    def entityWithFormat(self, conKey, schemaName, name, type, df):
        self.connectionKey = conKey
        self.schema = schemaName
        self.entityName = name
        self.entityType = type
        self.dataFormat = df

    def entity(self, conKey,  schemaName,  name, type):
        self.connectionKey = conKey
        self.schema = schemaName
        self.entityName = name
        self.entityType = type

    def stringValue(self, val):
        self.stringValue = val

    def build(self):
        key = getUuid(self.name)

        dataAssetType = "com.oracle.dicom.model.dataasset.AbstractDataAsset"
        connectionType = "com.oracle.dicom.model.connection.AbstractConnection"
        schemaType = "com.oracle.dicom.model.schema.Schema"
        ventityType = "com.oracle.dicom.model.entity.AbstractDataEntity"
        stringType = "java.lang.String"

        if (self.entityName is not None):
            jt = JavaType(java_type_name=ventityType)
            entitystr = "dataref:"+self.connectionKey+"/" + \
                self.schema+"/"+self.entityType+":"+self.entityName
            ee = None
            de = None
            if (self.entityType == "FILE_ENTITY"):
                de = DataEntityFromFile(
                    key=entitystr, object_status=1, entity_type=DataEntityFromFile.ENTITY_TYPE_FILE,
                    name=self.entityName, resource_name=self.entityName, data_format=self.dataFormat)
            else:
                de = DataEntityFromTable(
                    key=entitystr, object_status=1, entity_type=DataEntityFromTable.ENTITY_TYPE_TABLE, name=self.entityName, resource_name=self.entityName)

            if (self.dataFormat is not None):
                ee = EnrichedEntity(
                    entity=de, data_format=self.dataFormat, model_type="ENRICHED_ENTITY")
            else:
                ee = EnrichedEntity(entity=de, model_type="ENRICHED_ENTITY")
            return Parameter(name=self.name, key=key, root_object_default_value=ee, type=jt)
        elif (self.schema is not None):
            schemakey = "dataref:"+self.connectionKey+"/"+self.schema
            sch = Schema(key=schemakey, object_status=1,
                         name=self.schema, resource_name=self.schema)
            jt = JavaType(java_type_name=schemaType)
            return Parameter(name=self.name, key=key, root_object_default_value=sch, type=jt)
        elif (self.connectionKey is not None):
            jt = JavaType(java_type_name=connectionType)
            return Parameter(name=self.name, key=key, root_object_default_value=self.connectionKey, type=jt)
        elif (self.dataAssetKey is not None):
            jt = JavaType(java_type_name=dataAssetType)
            return Parameter(name=self.name, key=key, root_object_default_value=self.dataAssetKey, type=jt)
        elif (self.stringValue is not None):
            jt = JavaType(java_type_name=stringType)
            return Parameter(name=self.name, key=key, default_value=self.stringValue, type=jt)
        return None

    def buildValue(self, opName):
        key = getUuid(opName)
        if (self.entityName is not None):
            entitystr = "dataref:"+self.connectionKey+"/" + \
                self.schema+"/"+self.entityType+":"+self.entityName
            ee = None
            de = None
            shape = Shape(key=self.connectionKey+"/"+self.schema+"/" +
                          self.entityType+":"+self.entityName+"/SHAPE", type=CompositeType())
            if (self.entityType == "FILE_ENTITY"):
                de = DataEntityFromFile(
                    key=entitystr,
                    object_status=8,
                    entity_type=DataEntityFromFile.ENTITY_TYPE_FILE,
                    shape=shape,
                    name=self.entityName, resource_name=self.entityType+":"+self.entityName, data_format=self.dataFormat)
            else:
                de = DataEntityFromTable(
                    key=entitystr, object_status=8, entity_type=DataEntityFromTable.ENTITY_TYPE_TABLE, name=self.entityName, resource_name=self.entityType+":"+self.entityName)

            parentRef = ParentReference(parent=key)
            if (self.dataFormat is not None):
                ee = {"entity": de, "dataFormat": self.dataFormat,
                      "modelType": "ENRICHED_ENTITY", "parentRef": parentRef}
            else:
                ee = {"entity": de, "modelType": "ENRICHED_ENTITY",
                      "parentRef": parentRef}
            return ee
        return None
