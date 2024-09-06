# OCI Data Integration Common Tasks

## Prerequisites
You should have an OCI Data Integration workspace created and also a project within the workspace. You will need these to create the tasks below.

## Setup
Define the following environment variables and then execute the script to create the tasks in OCI DI.  Get the project key and the workspace and the region and set;
```
export PROJECTKEY=
export WORKSPACE_ID=
export REGION=us-ashburn-1
```

## Install via Script and OCI CLI
install.sh

## Install via Python and OCI Python SDK
python3 install.py workspaceid prokectkey us-ashburn-1

## Permissions

The theme for all of these permissions is to allow the disworkspace resource permission to perform the APIs concerned. The tasks have been defined using workspace resource BUT REST tasks can be defined to use workspace or application resource, application resource will give a tighter control. The example permissions can be further refined for example the specific operation can be added.

### Cloud Agent (OCI Compute) tasks
```
allow any-user to manage instance-agent-command-family in compartment <compartment-name> where ALL {request.principal.type='disworkspace’,request.principal.id='<workspace_ocid>’}
allow any-user to manage instance-agent-command-execution-family in compartment <compartment-name> where ALL {request.principal.type='disworkspace’,request.principal.id='<workspace_ocid>’}
```

### Container Instance tasks
```
allow any-user to manage compute-container-family in compartment yourcompartment where ALL {request.principal.type = 'disworkspace'}
```

### Data Science tasks
```
allow any-user to manage data-science-family in compartment yourcompartment where ANY {request.principal.type = 'disworkspace'}	
```

### Object Storage tasks
```
allow any-user to manage object-family in compartment yourcompartment where ANY {request.principal.type = 'disworkspace'}	
```

### AI Speech tasks
```
allow any-user to manage ai-service-speech-family in compartment yourcompartment where ALL {request.principal.type = 'disworkspace'}
```

### AI Vision tasks
```
allow any-user to manage ai-service-vision-family in compartment yourcompartment where ALL {request.principal.type = 'disworkspace'}
```

### AI Speech tasks
```
allow any-user to manage ai-service-speech-family in compartment yourcompartment where ALL {request.principal.type = 'disworkspace'}
```

### AI Document tasks
```
allow any-user to manage ai-service-document-family in compartment yourcompartment where ALL {request.principal.type = 'disworkspace'}
```

### NoSQL tasks
```
allow any-user to manage nosql-family in compartment yourcompartment where ALL {request.principal.type = 'disworkspace'}
```

### Monitoring tasks
```
allow any-user to read metrics in compartment yourcompartment where ALL {request.principal.type = 'disworkspace'}
```

### Notification tasks
```
allow any-user to use ons-topics in compartment yourcompartment where ALL {request.principal.type = 'disworkspace'}
```

### Dataflow tasks
```
allow any-user to manage dataflow-run in compartment yourcompartment where ALL {request.principal.type = 'disworkspace'}
```

### Data Integration tasks
```
allow any-user to use dis-workspaces in compartment yourcompartment where ALL {request.principal.type = 'disworkspace'}
```

### Generic REST executor

Whatever permissions are needed for the service you use you will need to add just like above using resource principal.
