#!/usr/bin/env python3

import sys
import boto3
import json

stackName = sys.argv[1]
regionName = sys.argv[2]
parametersFile = sys.argv[3]

cf = boto3.client('cloudformation', region_name = regionName)

vpcId = [o['OutputValue'] for o in cf.describe_stacks(StackName = stackName)['Stacks'][0]['Outputs'] if o['OutputKey'] == 'VpcId'][0]

parameters = json.loads(open(parametersFile, 'r').read())

found = False
for parameter in parameters:
  if parameter["ParameterKey"] == 'PeerVpcId':
    parameter["ParameterValue"] = vpcId
    found = True
    break

if not found:
  parameters.append({"ParameterKey": 'PeerVpcId', "ParameterValue": vpcId})

with open(parametersFile, 'w') as f:
  f.write(json.dumps(parameters, indent=2))
