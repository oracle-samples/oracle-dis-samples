#!/bin/sh

# Enter the project key and the workspace
#export PROJECTKEY=
#export WORKSPACE_ID=
#export REGION=

for FILE in src/tasks/*/*; do 
  echo $FILE
  rslt=$(cat $FILE | sed 's/{{PROJECT_KEY}}/'$PROJECTKEY'/g');
  oci raw-request --http-method POST --target-uri https://dataintegration.${REGION}.oci.oraclecloud.com/20200430/workspaces/$WORKSPACE_ID/tasks --request-body "$rslt";
done
