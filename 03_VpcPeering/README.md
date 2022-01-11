# Architecture using VPC peering

## Description
The Cloudformation template and script in this folder allow a customer create two VPCs in different regions.
This example is showing how to mount an S3 bucket in a remote region with respect to the Databricks workspace region.

## Example using the CLI

### Set the global parameters
cat > dbs-vpc-peering-parameters.json << EOF
[
  {
    "ParameterKey": "ResourceOwner", "ParameterValue": "<RESOURCE_OWNER>"
  },
  {
    "ParameterKey": "SourceRegion", "ParameterValue": "eu-west-3"
  },
  {
    "ParameterKey": "WorkspaceRegion", "ParameterValue": "eu-west-1"
  },
  {
    "ParameterKey": "DBSRootBucketName", "ParameterValue": "<ROOT_BUCKET_NAME>"
  },
  {
    "ParameterKey": "DBSVPCCidrBlock", "ParameterValue": "10.30.0.0/16"
  },
  {
    "ParameterKey": "DBSPublicSubnetCidrBlock", "ParameterValue": "10.30.0.0/24"
  },
  {
    "ParameterKey": "DBSPrivateSubnet1CidrBlock", "ParameterValue": "10.30.4.0/22"
  },
  {
    "ParameterKey": "DBSPrivateSubnet2CidrBlock", "ParameterValue": "10.30.8.0/22"
  },
  {
    "ParameterKey": "SrcVPCCidrBlock", "ParameterValue": "10.31.0.0/16"
  },
  {
    "ParameterKey": "SrcPrivateSubnet1CidrBlock", "ParameterValue": "10.31.4.0/22"
  },
  {
    "ParameterKey": "SrcPrivateSubnet2CidrBlock", "ParameterValue": "10.31.8.0/22"
  },
  {
    "ParameterKey": "DBSAccountId", "ParameterValue": "<DATABRICKS_ACCOUNT_ID>"
  },
  {
    "ParameterKey": "DBSUsername", "ParameterValue": "<DATABRICKS_USER_NAME>"
  },
  {
    "ParameterKey": "DBSPassword", "ParameterValue": "<DATABRICKS_PASSWORD>"
  }
]
EOF


### Create the VPC in the workspace region
aws \
--region eu-west-1 \
cloudformation create-stack \
--stack-name dbs-vpc-peering \
--capabilities CAPABILITY_NAMED_IAM \
--parameters file://dbs-vpc-peering-parameters.json \
--template-body file://dbs-vpc-peering.yml

### get the value of the VPC id and add it into the parameters file
./setPeerVpcId.py dbs-vpc-peering eu-west-1 dbs-vpc-peering-parameters.json

### Create the VPC in the source region. This sets up the peering and the private hosted zone
aws \
--region eu-west-3 \
cloudformation create-stack \
--stack-name dbs-vpc-peering \
--capabilities CAPABILITY_NAMED_IAM \
--parameters file://dbs-vpc-peering-parameters.json \
--template-body file://dbs-vpc-peering.yml

### get the value of the VPC peer connection id and add it into the parameters file
./setVpcPeeringConnectionId.py dbs-vpc-peering eu-west-3 dbs-vpc-peering-parameters.json

### Update the VPC in the workspace region
aws \
--region eu-west-1 \
cloudformation update-stack \
--stack-name dbs-vpc-peering \
--capabilities CAPABILITY_NAMED_IAM \
--parameters file://dbs-vpc-peering-parameters.json \
--template-body file://dbs-vpc-peering.yml

## Example of use

### Mound the bucket and access the data with Databricks
Import, edit, and run the Databricks notebook: MountAndUseRemoteBucket.py