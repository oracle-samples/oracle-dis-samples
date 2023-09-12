# Introduction

These scripts can be used to demonstrate the creation of OCI-DI Dataflows and Pipelines. It extends the SDK by providing a library that provides methods to create dataflow or pipeline nodes and parameters.  

## Sample Scripts 

1. [dis_dataflow_sample.py](https://github.com/oracle-samples/oracle-dis-samples/blob/main/python-samples/create_dataflow_pipelines_with_parameters/dis_dataflow_sample.py) - Creates a dataflow with a Source, Filter and Target nodes, using OCI Object Store as the data assets.


2. [dis_pipeline_sample.py](https://github.com/oracle-samples/oracle-dis-samples/blob/main/python-samples/create_dataflow_pipelines_with_parameters/dis_pipeline_sample.py) - Creates a sample pipeline with a Start and End nodes, two Integration tasks with a Merge operator. 
Set please the variables inside the script before executing.

### Example - dis_dataflow_sample.py

```python dis_dataflow_sample.py -h ``` 

```
usage: dis_dataflow_sample.py [-h] [-w WORKSPACE] [-i INPUT_FILE] [-o OUTPUT_FILE] [-df DATAFLOW_NAME] [-id DF_IDENTIFIER] [-s SOURCE_DA] [-sc SOURCE_CONN] [-t TARGET_DA] [-tc TARGET_CONN] [-f FOLDER] [-sh SCHEMA] [-p PROFILE]

optional arguments:
  -h, --help            show this help message and exit
  -w WORKSPACE, --workspace WORKSPACE
                        DIS workspace OCID; ocid1.disworkspace.oc1...
  -i INPUT_FILE, --input_file INPUT_FILE
                        Input file
  -o OUTPUT_FILE, --output_file OUTPUT_FILE
                        Output file
  -df DATAFLOW_NAME, --dataflow_name DATAFLOW_NAME
                        dataflow name
  -id DF_IDENTIFIER, --df_identifier DF_IDENTIFIER
                        dataflow ID
  -s SOURCE_DA, --source_da SOURCE_DA
                        Data Source Data Asset Key
  -sc SOURCE_CONN, --source_conn SOURCE_CONN
                        Data Source connection key
  -t TARGET_DA, --target_da TARGET_DA
                        Data Target Data Asset Key
  -tc TARGET_CONN, --target_conn TARGET_CONN
                        Data Target connection key
  -f FOLDER, --folder FOLDER
                        Folder Key
  -sh SCHEMA, --schema SCHEMA
                        Data Scema
  -p PROFILE, --profile PROFILE
                        Profile for ~/.oci/config
```
### Example - dis_pipeline_sample.py

```python dis_pipeline_sample.py -h ```

```
usage: dis_pipeline_sample.py [-h] [-w WORKSPACE] [-pn PIPELINE_NAME] [-id PIPELINE_IDENTIFIER] [-sc CONNECTION_KEY] [-a APPLICATION_KEY] [-t TASK_KEY] [-f FOLDER] [-p PROFILE]

optional arguments:
  -h, --help            show this help message and exit
  -w WORKSPACE, --workspace WORKSPACE
                        DIS workspace OCID; ocid1.disworkspace.oc1...
  -pn PIPELINE_NAME, --pipeline_name PIPELINE_NAME
                        pipeline name
  -id PIPELINE_IDENTIFIER, --pipeline_identifier PIPELINE_IDENTIFIER
                        Pipeline ID
  -sc CONNECTION_KEY, --connection_key CONNECTION_KEY
                        Connection key
  -a APPLICATION_KEY, --application_key APPLICATION_KEY
                        Application key
  -t TASK_KEY, --task_key TASK_KEY
                        Task key
  -f FOLDER, --folder FOLDER
                        Folder for the pipeline
  -p PROFILE, --profile PROFILE
                        Profile for ~/.oci/config
```