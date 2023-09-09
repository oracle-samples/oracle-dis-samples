#!/usr/bin/env python3

# Copyright © 2023, Oracle and/or its affiliates. 
# The Universal Permissive License (UPL), Version 1.0 as shown at https://oss.oracle.com/licenses/upl.


from oci.data_integration.models.composite_field_map import CompositeFieldMap
from oci.data_integration.models.config_values import ConfigValues
from oci.data_integration.models.config_parameter_value import ConfigParameterValue
from oci.data_integration.models.dynamic_input_field import DynamicInputField
from oci.data_integration.models.dynamic_type import DynamicType
from oci.data_integration.models.flow_node import FlowNode
from oci.data_integration.models.input_link import InputLink
from oci.data_integration.models.input_port import InputPort
from oci.data_integration.models.name_pattern_rule import NamePatternRule
from oci.data_integration.models.output_link import OutputLink
from oci.data_integration.models.output_port import OutputPort
from oci.data_integration.models.proxy_field import ProxyField
from oci.data_integration.models.dynamic_proxy_field import DynamicProxyField
from oci.data_integration.models.read_operation_config import ReadOperationConfig
from oci.data_integration.models.rule_type_config import RuleTypeConfig
from oci.data_integration.models.source import Source
from oci.data_integration.models.target import Target
from oci.data_integration.models.projection import Projection
from oci.data_integration.models.start_operator import StartOperator
from oci.data_integration.models.end_operator import EndOperator
from oci.data_integration.models.schema import Schema
from oci.data_integration.models.data_asset import DataAsset
from oci.data_integration.models.connection import Connection
from oci.data_integration.models.root_object import RootObject
from oci.data_integration.models.write_operation_config import WriteOperationConfig
from oci.data_integration.models.schema_drift_config import SchemaDriftConfig
from oci.data_integration.models.shape import Shape
from oci.data_integration.models.data_entity_from_file import DataEntityFromFile
from oci.data_integration.models.data_entity_from_table import DataEntityFromTable
from oci.data_integration.models.composite_type import CompositeType
from oci.data_integration.models.parent_reference import ParentReference
from oci.data_integration.models.oracle_adwc_write_attributes import OracleAdwcWriteAttributes

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


class FromObject:
    def __init__(self, node, link):
        self.node = node
        self.link = link


class ToObject:
    def __init__(self, node, link):
        self.node = node
        self.link = link


class OperatorProperty:
    def __init__(self, name, value):
        self.value = value
        self.name = name


"""

This helper creates Source and Target nodes and standard links/ports for these operators type.
The operator type is specified when the node is created.
Inputs / Outputs
Nodes have inputs and outputs, each operator type
Source has 0 inputs and one output.
The pattern for the input/output names is INPUTn/OUTPUTm
"""


class Node:
    def __init__(self, name, identifier, type):
        self.name = name
        self.identifier = identifier
        self.type = type
        self.operatorProperties = []
        self.fromObjects = []
        self.toObjects = []
        self.projectionRules = {}
        self.selectionRules = {}
        self._fieldMaps = []
        self._expressions = []
        self.modelType = ""

    def dataAsset(self, dataAssetType, dataAssetKey):
        self.operatorProperties.append(
            OperatorProperty("dataAsset", dataAssetKey))
        self.operatorProperties.append(
            OperatorProperty("dataAssetType", dataAssetType))

    def dataAssetParam(self, dataAssetType, dataAssetKey, parameterRef):
        self.operatorProperties.append(
            OperatorProperty("dataAsset", dataAssetKey))
        self.operatorProperties.append(
            OperatorProperty("dataAssetType", dataAssetType))
        self.operatorProperties.append(
            OperatorProperty("dataAssetReference", parameterRef))

    def connection(self, connectionType, connectionKey):
        self.operatorProperties.append(
            OperatorProperty("connection", connectionKey))
        self.operatorProperties.append(
            OperatorProperty("connectionType", connectionType))

    def connectionParam(self, connectionType, connectionKey, parameterRef):
        self.operatorProperties.append(
            OperatorProperty("connection", connectionKey))
        self.operatorProperties.append(
            OperatorProperty("connectionType", connectionType))
        self.operatorProperties.append(
            OperatorProperty("connectionReference", parameterRef))

    def schema(self, schema):
        self.operatorProperties.append(OperatorProperty("schema", schema))

    def schemaParam(self, schema, parameterRef):
        self.operatorProperties.append(OperatorProperty("schema", schema))
        self.operatorProperties.append(
            OperatorProperty("schemaReference", parameterRef))

    def entity(self, entityType, entityKey):
        self.operatorProperties.append(OperatorProperty("entity", entityKey))
        self.operatorProperties.append(
            OperatorProperty("entityType", entityType))

    def entityParam(self, entityType, entityKey, parameterRef):
        self.operatorProperties.append(OperatorProperty("entity", entityKey))
        self.operatorProperties.append(
            OperatorProperty("entityType", entityType))
        self.operatorProperties.append(
            OperatorProperty("entityReference", parameterRef))

    def parameterRef(self, parameterName, parameterRef):
        self.operatorProperties.append(OperatorProperty(
            parameterName + "Reference", parameterRef))

    def parameterValue(self, parameterBuild):
        self.operatorProperties.append(
            OperatorProperty(parameterBuild.name + "ParameterValue", parameterBuild.buildValue(self.name)))

    def operatorProperty(self, propName, propValue):
        self.operatorProperties.append(OperatorProperty(propName, propValue))

    def fromObject(self, fromObject, link):
        self.fromObjects.append(FromObject(fromObject, link))

    def toObject(self, toObject, link):
        self.toObjects.append(ToObject(toObject, link))

    def getOperatorProperty(self, property):
        for i in self.operatorProperties:
            if (i.name == property):
                return i.value
        return None

    def build(self):
        key = get_uuid()
        outflds = []
        primarySource = None
        if (self.type == "Minus" or self.type == "Union" or self.type == "Intersect"):
            primarySource = self.getOperatorProperty("primarySource")
            if (primarySource is None):
                primarySource = "INPUT1"
        if ((self.fromObjects is not None) and len(self.fromObjects) > 0):
            for i in range(len(self.fromObjects)):
                fldkeyi = getUuid(self.identifier + ".FIELD" + str(i + 1))
                scope = self.getScope(i + 1)

                rules = []
                rules = self.getProjectionRules(
                    self.selectionRules.get("INPUT" + str(i + 1)))
                rule_type_config = RuleTypeConfig(
                    scope=scope, projection_rules=rules)
                dynamic_type = DynamicType(type_handler=rule_type_config)
                if (len(rules) > 0):
                    outfld = DynamicProxyField(
                        key=fldkeyi, name="FIELD" + str(i + 1), type=dynamic_type)
                    outflds.append(outfld)
                else:
                    outfld = ProxyField(
                        key=fldkeyi, name="FIELD1", scope=scope)
                    outflds.append(outfld)

        else:
            scope = self.getScope(1)
            fldkey = getUuid(self.identifier + ".OUTPUT1.FIELD1")
            rules = []
            rules = self.getProjectionRules(
                self.projectionRules.get("OUTPUT1"))

            rule_type_config = RuleTypeConfig(
                scope=scope, projection_rules=rules)
            dynamic_type = DynamicType(type_handler=rule_type_config)
            if (len(rules) > 0):
                outfld = DynamicProxyField(
                    key=fldkey, name="FIELD1", type=dynamic_type)
                outflds.append(outfld)
            else:
                outfld = ProxyField(key=fldkey, name="FIELD1", scope=scope)
                outflds.append(outfld)
        if (self.type == "Projection"):
            for j in self._expressions:
                outflds.append(j)
        outputf_port = OutputPort(key=getUuid(self.identifier + ".OP1"),
                                  port_type=OutputPort.PORT_TYPE_DATA,
                                  name=self.identifier + "_OUT", fields=outflds)

        olkey = getUuid(self.identifier + ".OUTPUT1")
        opkey = getUuid(self.identifier + ".OP1")

        fieldMaps = None
        if (self.type == "Target"):
            fieldMaps = self.getFieldMaps()

        inputLinks = []
        inputPorts = []
        if ((self.fromObjects is not None) and len(self.fromObjects) > 0):
            for i in range(len(self.fromObjects)):
                ilkey = getUuid(self.identifier + ".INPUT" + str(i + 1))
                ipkey = getUuid(self.identifier + ".IP" + str(i + 1))
                fromLinkVal = getUuid(
                    self.fromObjects[i].node + "." + self.fromObjects[i].link)
                inputLink = InputLink(
                    key=ilkey, port=ipkey, from_link=fromLinkVal, field_map=fieldMaps)
                inputLinks.append(inputLink)

                difkey = getUuid(self.identifier + ".INPUT" +
                                 str(i + 1) + ".FIELD1")
                infld = self.createDynamicInputField(
                    "INPUT" + str(i + 1), difkey)
                inflds = []
                inflds.append(infld)
                inputPort = InputPort(key=getUuid(self.identifier + ".IP" + str(i + 1)),
                                      port_type=InputPort.PORT_TYPE_DATA,
                                      name=self.identifier + "_IN" + str(i + 1), fields=inflds)
                inputPorts.append(inputPort)
        outputLink = None
        outputLinks = []
        outputPorts = []
        if ((self.toObjects is not None) and len(self.toObjects) > 0):
            toLinksVal = []
            for i in range(len(self.toObjects)):
                lnkkey = getUuid(
                    self.toObjects[i].node + "." + self.toObjects[i].link)
                toLinksVal.append(lnkkey)
            outputLink = OutputLink(key=olkey, port=opkey, to_links=toLinksVal)
            outputLinks = [outputLink]
            outputPorts = [outputf_port]

        operator = None
        if (self.type == "Start"):
            operator = self.create_start(
                self.name, self.identifier, inputPorts, outputPorts)
        elif (self.type == "End"):
            operator = self.create_end(
                self.name, self.identifier, inputPorts, outputPorts)
        elif (self.type == "Source"):
            operator = self.create_source(
                self.name, self.identifier, inputPorts, outputPorts)
        elif (self.type == "Target"):
            operator = self.create_target(
                self.name, self.identifier, inputPorts, outputPorts)
        elif (self.type == "Projector"):
            operator = self.create_projection(
                self.name, self.identifier, inputPorts, outputPorts)
        return FlowNode(key=key, name=self.name, input_links=inputLinks, operator=operator, output_links=outputLinks)

    def getFieldMaps(self):
        composite_field_map = CompositeFieldMap(field_maps=self._fieldMaps)
        return composite_field_map

    def createDynamicInputField(self, difName, difKey):
        name_pattern_rule = NamePatternRule(matching_strategy=NamePatternRule.MATCHING_STRATEGY_NAME_ONLY,
                                            rule_type=NamePatternRule.RULE_TYPE_INCLUDE, pattern=".*")
        rules = []
        rules = self.getProjectionRules(self.selectionRules.get(difName))
        scope = None
        if (len(rules) == 0):
            rules.append(name_pattern_rule)
        if (self.type == "Target"):
            scope = self.getScope(1)
        rule_type_config = RuleTypeConfig(scope=scope, projection_rules=rules)
        dynamic_type = DynamicType(type_handler=rule_type_config)
        return DynamicInputField(key=difKey, name=difName, type=dynamic_type)

    def getScope(self, inputNumber):
        if (self.type == "Source" or self.type == "Target"):
            self.model_type = "FLOW_NODE"
            sconnection = None
            sschema = None
            sentityType = None
            sentity = None
            createNewEntity = False
            for i in range(len(self.operatorProperties)):
                if (self.operatorProperties[i].name == "connection"):
                    sconnection = self.operatorProperties[i].value
                if (self.operatorProperties[i].name == "schema"):
                    sschema = self.operatorProperties[i].value
                if (self.operatorProperties[i].name == "entity"):
                    sentity = self.operatorProperties[i].value
                if (self.operatorProperties[i].name == "entityType"):
                    sentityType = self.operatorProperties[i].value
                if (self.operatorProperties[i].name == "createNewEntity"):
                    createNewEntity = self.operatorProperties[i].value
            if (createNewEntity is None or createNewEntity is True):
                if len(self.fromObjects) > 0:
                    return getUuid(self.fromObjects[0].node + ".OP1")
                return None
            if (sentity is None or sentityType is None):
                raise Exception('Entity is not set for operator', self.name)
            if (sschema is None or sconnection is None):
                raise Exception(
                    'Connection/Schema are not set for operator', self.name)
            return sconnection + "/" + sschema + "/" + sentityType + ":" + sentity + "/SHAPE"

        else:
            return getUuid(self.identifier + ".INPUT" + str(inputNumber) + ".FIELD1")

    def getProjectionRules(self, vRules):
        rules = []
        if (vRules is not None and len(vRules) > 0):
            for r in range(len(vRules)):
                rules.append(vRules[r])
        return rules

    def getDataEntity(self, opKey):
        sconnection = None
        sschema = None
        sentity = None
        sentityType = None
        dataFormat = None
        createNewEntity = False
        for i in self.operatorProperties:
            if (i.name == "connection"):
                sconnection = i.value
            if (i.name == "schema"):
                sschema = i.value
            if (i.name == "entity"):
                sentity = i.value
            if (i.name == "entityType"):
                sentityType = i.value
            if (i.name == "dataFormat"):
                dataFormat = i.value
            if (i.name == "createNewEntity"):
                createNewEntity = i.value
        srcEntity = None
        shape = None
        objectStatus = 8
        parentRef = None
        de = None
        if (createNewEntity is False):
            shape = Shape(key=sconnection + "/" + sschema + "/" + sentityType + ":" + sentity + "/SHAPE",
                          type=CompositeType())
            srcEntity = "dataref:" + sconnection + "/" + \
                sschema + "/" + sentityType + ":" + sentity
            resourceName = sentityType + ":" + sentity
        else:
            resourceName = sentity
            parentRef = ParentReference(parent=opKey)

        if (sentityType == "FILE_ENTITY"):
            if (createNewEntity is False):
                objectStatus = 0
            de = DataEntityFromFile(
                key=srcEntity, object_status=objectStatus, entity_type=DataEntityFromFile.ENTITY_TYPE_FILE,
                name=sentity, resource_name=resourceName, data_format=dataFormat,
                shape=shape,
                parent_ref=parentRef)
        else:
            if (createNewEntity is False):
                objectStatus = 0
            de = DataEntityFromTable(
                key=srcEntity, object_status=objectStatus, entity_type=DataEntityFromTable.ENTITY_TYPE_TABLE,
                name=sentity, resource_name=resourceName,
                shape=shape,
                parent_ref=parentRef)
        return de

    def getConfigValuesMap(self):
        sdataAsset = None
        sconnection = None
        sschema = None
        sschemaReference = None
        sconnectionReference = None
        sdataAssetReference = None
        sdataAssetType = None
        sconnectionType = None
        scustomReference = None
        scustomParameter = None
        scustomValue = None
        allowPushdown = None
        configValuesMap = {}
        for i in self.operatorProperties:
            if (i.name == "dataAsset"):
                sdataAsset = i.value
            elif (i.name == "connection"):
                sconnection = i.value
            elif (i.name == "schema"):
                sschema = i.value
            elif (i.name == "schemaReference"):
                sschemaReference = i.value
            elif (i.name == "connectionReference"):
                sconnectionReference = i.value
            elif (i.name == "dataAssetReference"):
                sdataAssetReference = i.value
            elif (i.name == "dataAssetType"):
                sdataAssetType = i.value
            elif (i.name == "connectionType"):
                sconnectionType = i.value
            elif (i.name == "allowPushdown"):
                allowPushdown = not (i.value)
            elif (i.name.endswith("Reference")):
                scustomParameter = i.value
                scustomReference = i.name.removesuffix("Reference")
            elif (i.name.endswith("ParameterValue")):
                scustomValue = i.value
                scustomReference = i.name.removesuffix("ParameterValue")

            if (sconnectionReference is not None):
                conParam = getUuid(sconnectionReference)
                configValuesMap["connectionParam"] = ConfigParameterValue(
                    parameter_value=conParam)
            elif (sconnection is not None):
                con = RootObject(model_type=sconnectionType,
                                 key=sconnection, object_status=1)
                configValuesMap["connectionParam"] = ConfigParameterValue(
                    ref_value=con)
            if (sdataAssetReference is not None):
                daParam = getUuid(sdataAssetReference)
                configValuesMap["dataAssetParam"] = ConfigParameterValue(
                    parameter_value=daParam)
            elif (sdataAsset is not None):
                dataasset = RootObject(
                    model_type=sdataAssetType, key=sdataAsset, object_status=1)
                configValuesMap["dataAssetParam"] = ConfigParameterValue(
                    ref_value=dataasset)
            if (sschemaReference is not None):
                schemaParam = getUuid(sschemaReference)
                configValuesMap["schemaParam"] = ConfigParameterValue(
                    parameter_value=schemaParam)
            elif (sschema is not None):
                schema = Schema(model_type="SCHEMA", key="dataref:" +
                                sconnection + "/" + sschema, name=sschema)
                configValuesMap["schemaParam"] = ConfigParameterValue(
                    ref_value=schema)
            if (allowPushdown is not None):
                configValuesMap["disablePushDownParam"] = ConfigParameterValue(
                    object_value=allowPushdown)
            if (scustomParameter is not None):
                customParamRef = getUuid(scustomParameter)
                configValuesMap[scustomReference] = {
                    "modelType": "CONFIG_PARAMETER_VALUE", "refValue": customParamRef}
            if (scustomValue is not None):
                configValuesMap[scustomReference] = {"modelType": "CONFIG_PARAMETER_VALUE",
                                                     "rootObjectValue": scustomValue}
        return configValuesMap

    def getConfigValues(self):
        configValuesMap = self.getConfigValuesMap()
        default_config = ConfigValues(config_param_values=configValuesMap)
        return default_config

    def create_start(self, name, identifier, input_ports, output_ports):
        key = get_uuid()
        op = StartOperator(key=key, name=name, identifier=identifier, input_ports=input_ports,
                           output_ports=output_ports)
        return op

    def create_end(self, name, identifier, input_ports, output_ports):
        key = get_uuid()
        op = EndOperator(key=key, name=name, identifier=identifier,
                         input_ports=input_ports, output_ports=output_ports)
        return op

    def create_source(self, name, identifier, input_ports, output_ports):
        key = get_uuid()
        dataFormat = None
        sdc = SchemaDriftConfig(missing_column_handling=SchemaDriftConfig.MISSING_COLUMN_HANDLING_ALLOW,
                                extra_column_handling=SchemaDriftConfig.EXTRA_COLUMN_HANDLING_ALLOW,
                                data_type_change_handling=SchemaDriftConfig.DATA_TYPE_CHANGE_HANDLING_ALLOW,
                                is_validation_warning_if_allowed=True)
        for i in self.operatorProperties:
            if (i.name == "dataFormat"):
                dataFormat = i.value
            if (i.name == "allowSchemaDrift"):
                if (i.value is False):
                    sdc = SchemaDriftConfig(
                        missing_column_handling=SchemaDriftConfig.MISSING_COLUMN_HANDLING_DO_NOT_ALLOW,
                        extra_column_handling=SchemaDriftConfig.EXTRA_COLUMN_HANDLING.DO_NOT_ALLOW,
                        data_type_change_handling=SchemaDriftConfig.DATA_TYPE_CHANGE_HANDLING.DO_NOT_ALLOW,
                        is_validation_warning_if_allowed=False)

        de = self.getDataEntity(key)
        default_config = self.getConfigValues()
        readOperationConfig = ReadOperationConfig(data_format=dataFormat)

        op = Source(key=key, op_config_values=default_config, entity=de, name=name, identifier=identifier,
                    read_operation_config=readOperationConfig, input_ports=input_ports,
                    output_ports=output_ports,
                    schema_drift_config=sdc)
        return op

    def create_target(self, name, identifier, input_ports, output_ports):
        key = get_uuid()
        dataFormat = None
        is_predefined_shape = True
        is_copy_fields = False
        stagingDataAsset = None
        stagingConnection = None
        stagingBucket = None
        writeMode = WriteOperationConfig.WRITE_MODE_APPEND
        for i in self.operatorProperties:
            if (i.name == "dataFormat"):
                dataFormat = i.value
            if (i.name == "integrationStrategy"):
                vintegrationStrategy = i.value
                if (vintegrationStrategy == "OVERWRITE"):
                    writeMode = WriteOperationConfig.WRITE_MODE_OVERWRITE
                elif (vintegrationStrategy == "MERGE"):
                    writeMode = WriteOperationConfig.WRITE_MODE_MERGE
            if (i.name == "createNewEntity"):
                if (i.value is True):
                    is_predefined_shape = False
                    is_copy_fields = True
            if (i.name == "stagingDataAsset"):
                stagingDataAsset = i.value
            if (i.name == "stagingConnection"):
                stagingConnection = i.value
            if (i.name == "stagingBucket"):
                stagingBucket = i.value
        de = self.getDataEntity(key)
        default_config = self.getConfigValues()
        writeAttribute = None
        ky = None
        wokey = get_uuid()

        if (stagingBucket is not None):
            if (stagingConnection is not None and stagingDataAsset is not None):
                writeAttribute = OracleAdwcWriteAttributes(
                    bucket_schema=Schema(
                        name=stagingBucket, key="dataref:" + stagingConnection + "/" + stagingBucket),
                    staging_connection=Connection(key=stagingConnection, object_status=1,
                                                  model_type="ORACLE_OBJECT_STORAGE_CONNECTION"),
                    staging_data_asset=DataAsset(key=stagingDataAsset, object_status=1,
                                                 model_type="ORACLE_OBJECT_STORAGE_DATA_ASSET"))
            else:
                raise Exception('stagingBucket also needs stagingConnection and stagingDataAsset set on node',
                                self.name)
        writeOperationConfig = WriteOperationConfig(key=wokey, write_mode=writeMode, data_format=dataFormat,
                                                    write_attribute=writeAttribute, merge_key=ky)

        op = Target(is_predefined_shape=is_predefined_shape, is_copy_fields=is_copy_fields, key=key,
                    op_config_values=default_config, entity=de, name=name, identifier=identifier,
                    write_operation_config=writeOperationConfig, input_ports=input_ports, output_ports=output_ports)
        return op

    def create_projection(self, name, identifier, input_ports, output_ports):
        key = get_uuid()
        op = Projection(key=key, name=name, identifier=identifier,
                        input_ports=input_ports, output_ports=output_ports)
        return op
