resource "null_resource" "get_dis_template_keys" {
  depends_on = [oci_dataintegration_workspace.dis_workspace, oci_dataintegration_workspace_project.dis_workspace_project]
  provisioner "local-exec" {
    command = <<EOT
oci raw-request --target-uri https://dataintegration.${var.region}.oci.oraclecloud.com/20200430/workspaces/${oci_dataintegration_workspace.dis_workspace.id}/templates --http-method GET | \
jq  '{templates:[ .data.items[] | { "definedTags": {}, "freeformTags": {}, "sourceApplicationInfo": { "applicationKey": .key, "copyType": "DISCONNECTED" }, "modelType": "INTEGRATION_APPLICATION", "compartmentId": "${var.compartment_ocid}", "name": .name, "identifier": .identifier, "description": .description} ]}' > ${path.module}/metadata/dis_templates1.json
EOT
    working_dir = "${path.module}"
    interpreter = ["/bin/bash", "-c"] 
  }
    triggers = {
    template_file = "${path.module}/metadata/dis_templates1.json"
  }
}

locals {
  python = (substr(pathexpand("~"), 0, 1) == "/") ? "python3" : "python.exe"
}

resource "null_resource" "load_templates" {
  depends_on = [
    oci_dataintegration_workspace.dis_workspace,
    oci_dataintegration_workspace_project.dis_workspace_project,
    null_resource.get_dis_template_keys]

    provisioner "local-exec" {
    command = <<EOT
python3 scripts/createTemplates.py ${oci_dataintegration_workspace.dis_workspace.id} ${var.compartment_ocid} ${var.region}
EOT
    working_dir = "${path.module}"
    interpreter = [
      "/bin/bash", "-c"
    ]
  }

}
