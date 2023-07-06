## Copyright (c) 2022, Oracle and/or its affiliates.
## All rights reserved. The Universal Permissive License (UPL), Version 1.0 as shown at http://oss.oracle.com/licenses/upl

# DIS Policies
resource "oci_identity_policy" "DISWorkspaceManageAccessPolicy" {
  provider       = oci.homeregion
  name           = "DISWorkspaceManageAccessPolicy-${random_id.tag.hex}"
  description    = "DISWorkspaceManageAccessPolicy-${random_id.tag.hex}"
  compartment_id = var.compartment_ocid
  statements = ["Allow group ${var.DISadmingroup} to manage dis-workspaces in compartment id ${var.compartment_ocid}",
  "Allow group ${var.DISadmingroup} to read metrics in compartment id ${var.compartment_ocid}"]
  provisioner "local-exec" {
    command = "sleep 5"
  }
}

resource "oci_identity_policy" "DISNetworkAccessPolicy" {
  provider       = oci.homeregion
  name           = "DISManageNetworkAccessPolicy-${random_id.tag.hex}"
  description    = "DISManageNetworkAccessPolicy-${random_id.tag.hex}"
  compartment_id = var.tenancy_ocid
  statements     = ["Allow service dataintegration to use virtual-network-family in tenancy"]

  provisioner "local-exec" {
    command = "sleep 5"
  }
}

resource "oci_identity_policy" "DISObjectStorageManageAccessPolicy" {
  depends_on = [oci_dataintegration_workspace.dis_workspace, oci_dataintegration_workspace_project.dis_workspace_project]
  provider       = oci.homeregion
  name           = "DISObjectStorageManageAccessPolicy-${random_id.tag.hex}"
  description    = "DISObjectStorageManageAccessPolicy-${random_id.tag.hex}"
  compartment_id = var.tenancy_ocid
  statements     = ["Allow any-user to use buckets in compartment id ${var.compartment_ocid}  where ALL {request.principal.type = 'disworkspace', request.principal.id = ${oci_dataintegration_workspace.dis_workspace.id}}",
  "Allow any-user to manage objects in compartment id ${var.compartment_ocid}  where ALL {request.principal.type = 'disworkspace', request.principal.id = ${oci_dataintegration_workspace.dis_workspace.id}}",
  "Allow any-user to manage buckets in compartment id ${var.compartment_ocid}  where ALL {request.principal.type = 'disworkspace', , request.principal.id = ${oci_dataintegration_workspace.dis_workspace.id}, request.permission = 'PAR_MANAGE'}"]

  provisioner "local-exec" {
    command = "sleep 5"
  }
}

resource "oci_identity_policy" "DISVault" {
  depends_on = [oci_dataintegration_workspace.dis_workspace, oci_dataintegration_workspace_project.dis_workspace_project]
  provider       = oci.homeregion
  name           = "DISVault-${random_id.tag.hex}"
  description    = "DISVault-${random_id.tag.hex}"
  compartment_id = var.tenancy_ocid
  statements     = ["allow any-user to read secret-bundles in compartment id ${var.compartment_ocid}  where ALL {request.principal.type = 'disworkspace', request.principal.id = ${oci_dataintegration_workspace.dis_workspace.id}}"]
  provisioner "local-exec" {
    command = "sleep 5"
  }
}

resource "oci_identity_policy" "DISADB" {
  depends_on = [oci_dataintegration_workspace.dis_workspace, oci_dataintegration_workspace_project.dis_workspace_project]
  provider       = oci.homeregion
  name           = "DISADB-${random_id.tag.hex}"
  description    = "DISADB-${random_id.tag.hex}"
  compartment_id = var.tenancy_ocid
  statements     = ["allow any-user to manage buckets in compartment id ${var.compartment_ocid} where ALL {request.principal.type = 'disworkspace', request.principal.id = ${oci_dataintegration_workspace.dis_workspace.id}, request.permission = 'PAR_MANAGE'}"]
  provisioner "local-exec" {
    command = "sleep 5"
  }
}

resource "oci_identity_dynamic_group" "dis_dynamic_group" {
    #Required
    compartment_id = var.tenancy_ocid
    description = "DIS Dynamic Group"
    matching_rule = "ALL{resource.type = 'disworkspace', resource.compartment.id = ${var.compartment_ocid}}"
    name = "DISDynamicGroup"
}

resource "oci_identity_policy" "DIS_Templates" {
  depends_on = [oci_dataintegration_workspace.dis_workspace, oci_dataintegration_workspace_project.dis_workspace_project, oci_identity_dynamic_group.dis_dynamic_group]
  provider       = oci.homeregion
  name           = "DISTemplate"
  description    = "OCI Services Policy for DIS Templates"
  compartment_id = var.tenancy_ocid
  statements     = ["allow any-user to manage object-store-family in tenancy where ALL {request.principal.type = 'disapplication'}",
  "allow dynamic-group DISDynamicGroup to use ai-service-vision-family in tenancy",
  "allow dynamic-group DISDynamicGroup to use virtual-network-family in tenancy" ,
  "allow dynamic-group DISDynamicGroup to manage data-safe-discovery-family in tenancy",
  "allow dynamic-group DISDynamicGroup to manage data-safe-masking-policies in tenancy",
  "allow dynamic-group DISDynamicGroup to manage data-safe-masking-reports in tenancy",
  "allow dynamic-group DISDynamicGroup to read data-safe-work-requests in tenancy",
  "allow dynamic-group DISDynamicGroup to read target-databases in tenancy"]
  provisioner "local-exec" {
    command = "sleep 5"
  }
}

