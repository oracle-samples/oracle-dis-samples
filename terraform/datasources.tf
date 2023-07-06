## Copyright (c) 2022, Oracle and/or its affiliates.
## All rights reserved. The Universal Permissive License (UPL), Version 1.0 as shown at http://oss.oracle.com/licenses/upl

data "oci_identity_region_subscriptions" "home_region_subscriptions" {
  tenancy_id = var.tenancy_ocid

  filter {
    name   = "is_home_region"
    values = [true]
  }
}

data "oci_identity_regions" "oci_regions" {

  filter {
    name   = "name"
    values = [var.region]
  }

}

data "oci_identity_tenancy" "oci_tenancy" {
  tenancy_id = var.tenancy_ocid
}

data "oci_objectstorage_namespace" "test_namespace" {
  compartment_id = var.tenancy_ocid
}

data "oci_dataintegration_workspace_folders" "dis_workspace_folders" {
    #Required
    workspace_id = oci_dataintegration_workspace.dis_workspace.id
    aggregator_key = data.oci_dataintegration_workspace_projects.dis_workspace_projects.id

}
data "oci_dataintegration_workspace_projects" "dis_workspace_projects" {
    #Required
    workspace_id = oci_dataintegration_workspace.dis_workspace.id
}
