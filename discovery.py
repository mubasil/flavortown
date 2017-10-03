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
 

#add all files in recipe directory
directory = os.path.join(os.getcwd(), 'recipes2')
for filename in os.listdir(directory):
     #print filename
     with open(os.path.join(directory, filename)) as fileinfo:
         add_doc = discovery.add_document('0a15c836-8ec9-41ca-a33b-93a9d63dae8d', 
            '7844f79c-c259-4a3d-a2d8-2db7d18acd76',
             file_info=fileinfo)
