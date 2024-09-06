import oci
import json
import requests
import sys
import glob
import os
from oci.signer import Signer

config = oci.config.from_file('~/.oci/config')
# For raw-requests, get the signer auth
auth = Signer(
    tenancy=config['tenancy'],
    user=config['user'],
    fingerprint=config['fingerprint'],
    private_key_file_location=config['key_file']
)

data_integration_client = oci.data_integration.DataIntegrationClient(config)

workspaceID = sys.argv [1]
projectKey = sys.argv[2]
region = sys.argv[3]

url = 'https://dataintegration.' + region + '.oci.oraclecloud.com/20200430/workspaces/' + workspaceID + '/tasks'

path = "src/tasks/**"

for path in glob.glob(path, recursive=True):
 if path.endswith('.json'):
    print(path)
    with open(path, 'r') as file:
      filedata = file.read()
      filedata = filedata.replace('{{PROJECT_KEY}}', projectKey)
      payload=json.loads(filedata)
      response = requests.post(url, auth=auth, json=payload)
      print('Request response: ')
      print(json.loads(response.content.decode('utf8')))

