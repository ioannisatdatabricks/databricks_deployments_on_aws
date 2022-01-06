#!/usr/bin/env python3
import json
import sys

parameterFile = sys.argv[1]
parameterKey = sys.argv[2]
parameterValue = sys.argv[3]

parameters = json.loads(open(parameterFile, 'r').read())
for parameter in parameters:
  if parameter["ParameterKey"] == parameterKey:
    parameter["ParameterValue"] = parameterValue
    break
json.dump(parameters, open(parameterFile, 'w'))
