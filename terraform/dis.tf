resource "oci_dataintegration_workspace" "dis_workspace" {
    #depends_on = [oci_identity_group.DISManage]
    #Required
    compartment_id = var.compartment_ocid
    display_name = var.workspace_display_name

    #Optional
    #defined_tags = {"Operations.CostCenter"= "42"}
    #freeform_tags = {"Department"= "Finance"}
    is_private_network_enabled = var.workspace_is_private_network_enabled
    subnet_id = var.workspace_subnet_id
    vcn_id = var.workspace_vcn_id
}


resource "oci_dataintegration_workspace_project" "dis_workspace_project" {
    #Required
    workspace_id = oci_dataintegration_workspace.dis_workspace.id
    identifier = var.workspace_project_identifier
    name = var.workspace_project_name
    depends_on = [oci_dataintegration_workspace.dis_workspace]

    #Optional
    description = var.workspace_project_description
}

resource "oci_dataintegration_workspace_folder" "dis_workspace_folder" {
    #Required
    identifier = var.workspace_project_folder_identifier
    name = var.workspace_project_folder_name
    depends_on = [oci_dataintegration_workspace.dis_workspace, oci_dataintegration_workspace_project.dis_workspace_project]
    registry_metadata {

        #Optional
	aggregator_key = oci_dataintegration_workspace_project.dis_workspace_project.key
    }
    workspace_id = oci_dataintegration_workspace.dis_workspace.id

}
