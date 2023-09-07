# Introduction

These scripts can be used to demonstrate the creation of OCI-DI Dataflows and Pipelines. It extends the SDK by providing a library that provides methods to create dataflow or pipeline nodes and parameters.  

# Sample Scripts 

1. [dis_dataflow_sample.py](https://github.com/oracle-samples/oracle-dis-samples/blob/main/python-samples/create_dataflow_pipelines_with_parameters/dis_dataflow_sample.py) - Creates a dataflow with a Source, Filter and Target nodes, using OCI Object Store as the data assets.

Script parameters:
* --workspace= Workspace OCID
* --inputfile= Input filename
* --outputfile= Output filename
* --df_name= dataflow name
* --df_identifier= dataflow identifier
* --source_da= Source Data Asset key (OCI Object Store)
* --target_da= Target Data Asset key (OCI Object Store)
* --source_conn= Source Data Asset Connection key
* --target_conn= Target Data Asset Connection key
* --folder_id= OCI-DI Project or Folder key
*  --schema= OCI Object Store bucket

2. [dis_pipeline_sample.py](https://github.com/oracle-samples/oracle-dis-samples/blob/main/python-samples/create_dataflow_pipelines_with_parameters/dis_pipeline_sample.py) - Creates a sample pipeline with a Start and End nodes, two Integration tasks with a Merge operator. 
Set please the variables inside the script before executing.

## Example - dis_dataflow_sample.py

```python dis_dataflow_sample.py --workspace=WorskpaceOCID --inputfile=Sample_file.csv --outputfile=Processed_file.csv --df_name="SAMPLEDATAFLOW" --df_identifier="SAMPLEDATAFLOW" --source_da=SourceDAKey --target_da=TargetDAKey --source_conn=SourceConnKey --target_conn=TargetConnKey --folder_id=FolderKey --schema=OOSBucket```

