
import oci
import json
import requests
import sys
from oci.signer import Signer


###########################################################################################################################
# Start here
###########################################################################################################################

config = oci.config.from_file('~/.oci/config')
# For raw-requests, get the signer auth
auth = Signer(
    tenancy=config['tenancy'],
    user=config['user'],
    fingerprint=config['fingerprint'],
    private_key_file_location=config['key_file']
)

data_integration_client = oci.data_integration.DataIntegrationClient(config)
print(data_integration_client)

print(sys.argv)
workspaceID = sys.argv [1]
compartmentID = sys.argv[2]
region = sys.argv[3]

url = 'https://dataintegration.' + region + '.oci.oraclecloud.com/20200430/workspaces/' + workspaceID + '/disApplications'

with open('metadata/dis_templates1.json') as json_input:
  template_data = json.load(json_input)
  for template in template_data:
      for i, val in enumerate(template_data[template]):
        print ('Creating template : ' + template_data[template][i]['name'])
        template_request = requests.post(url, auth=auth, json=template_data[template][i])
        print('Request response: ')
        print(json.loads(template_request.content.decode('utf8')))

