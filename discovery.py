import sys
import os
import json
from watson_developer_cloud import DiscoveryV1

#api refrence: https://www.ibm.com/watson/developercloud/discovery/api/v1/

#Replace with your own credentials
discovery = DiscoveryV1(
  username='ff7c4fbe-e752-4c91-b99e-7f7db797e294',
  password='E3qe7yeI5Nrf',
  version='2017-09-01')

#create new environment
#ignore 'size_not_supported' warning
new_environment = discovery.create_environment(name="My_Environment", 
    description="My Environment", size=1)
print(json.dumps(new_environment, indent=2))
environment_id = new_environment['environment_id']

#create new colletion
new_collection = discovery.create_collection(environment_id, 'flavortown', 
    description='flavortown recipe collection')
print(json.dumps(new_collection, indent=2))
collection_id = new_collection['collection_id']
configuration_id = new_collection['configuration_id']

#add single file to collection
with open(os.path.join(os.getcwd(),'recipes/Tiger Tea.json')) as fileinfo:
    add_doc = discovery.add_document(environment_id, collection_id, 
        file_info=fileinfo)
print(json.dumps(add_doc, indent=2))   

#add all files in recipe directory
# directory = os.path.join(os.getcwd(), 'recipes')
# for filename in os.listdir(directory):
#     #print filename
#     with open(os.path.join(directory, filename)) as fileinfo:
#         add_doc = discovery.add_document(environment_id, collection_id, 
#             file_info=fileinfo)