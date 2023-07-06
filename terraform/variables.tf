## Copyright (c) 2022 Oracle and/or its affiliates.
## All rights reserved. The Universal Permissive License (UPL), Version 1.0 as shown at http://oss.oracle.com/licenses/upl

variable "tenancy_ocid" {}
variable "user_ocid" {}
variable "fingerprint" {}
variable "private_key_path" {}
variable "compartment_ocid" {}
variable "region" {}

variable "release" {
  description = "Reference Architecture Release (OCI Architecture Center)"
  default     = "1.0.0"
}

variable "ADW_database_password" {}

variable "db-schema" {
  default = "admin"
}

variable "db-user" {
  default = "admin"
}

variable "input-bucket" {
  default = "input-bucket"
}

variable "processed-bucket" {
  default = "processed-bucket"
}

variable "use_existing_vcn" {
  default = true
}

variable "VCN-CIDR" {
  default = "10.0.0.0/16"
}

variable "vcn_id" {
  default = ""
}

variable "fnsubnet-CIDR" {
  default = "10.0.1.0/24"
}

variable "fnsubnet_id" {
  default = ""
}

variable "ADW_database_cpu_core_count" {
  default = 1
}

variable "ADW_database_data_storage_size_in_tbs" {
  default = 1
}

variable "ADW_database_db_name" {
  default = "ADWDB1"
}

variable "ADW_database_db_version" {
  default = "19c"
}

variable "ADW_database_defined_tags_value" {
  default = ""
}

variable "ADW_database_display_name" {
  default = "ADWDB1"
}

variable "ADW_database_freeform_tags" {
  default = {
    "Owner" = ""
  }
}

variable "ADW_database_license_model" {
  default = "LICENSE_INCLUDED"
}

# DIS

variable "DISadmingroup" {}
variable "workspace_display_name" {}
variable "workspace_is_private_network_enabled" {}
variable "workspace_subnet_id" {}
variable "workspace_vcn_id" {}
variable "workspace_project_identifier" {}
variable "workspace_project_name" {}
variable "workspace_project_description" {}
variable "workspace_project_folder_identifier" {}
variable "workspace_project_folder_name" {}
variable "workspace_project_folder_description" {}


