# Baseline Architecture and deployment on AWS and Databricks

## Description
The Cloudformation template and script in this folder allow a customer create two buckets in different regions, which are cross-replicated, so that one of them can be mounted on DBFS.

## Prerequisites
- An existing Databricks deployment on AWS

## Example using the CLI

### Define the global parameters for the setup
cat > dbs-s3-bidirectional-crr-solution-parameters.json << EOF
[
  {
    "ParameterKey": "ResourceOwner",
    "ParameterValue": "ioannis.papadopoulos@databricks.com"
  },
  {
    "ParameterKey": "SourceRegion",
    "ParameterValue": "eu-west-3"
  },
  {
    "ParameterKey": "SourceDataBucketName",
    "ParameterValue": "dbs-ioannis-s3-bidirectional-crr-solution-source-bucket"
  },
  {
    "ParameterKey": "WorkspaceRegion",
    "ParameterValue": "eu-west-1"
  },
  {
    "ParameterKey": "WorkspaceBucketName",
    "ParameterValue": "dbs-ioannis-s3-bidirectional-crr-solution-workspace-bucket"
  },
  {
    "ParameterKey": "EstablishReplication",
    "ParameterValue": "no"
  }
]
EOF

### Create the bucket in the workspace region
aws --region eu-west-1 \
cloudformation create-stack \
--stack-name dbs-s3-bidirectional-crr-solution-data \
--capabilities CAPABILITY_NAMED_IAM \
--parameters file://dbs-s3-bidirectional-crr-solution-parameters.json \
--template-body file://dbs-s3-bidirectional-crr-solution.yml

### Update the config file so that EstablishReplication is set to yes from now onwards
./updateCfnParameter.py dbs-s3-bidirectional-crr-solution-parameters.json EstablishReplication yes

### Create the bucket in the source region. This will set up replication to the bucket in the workspace region
aws --region eu-west-3 \
cloudformation create-stack \
--stack-name dbs-s3-bidirectional-crr-solution-data \
--capabilities CAPABILITY_NAMED_IAM \
--parameters file://dbs-s3-bidirectional-crr-solution-parameters.json \
--template-body file://dbs-s3-bidirectional-crr-solution.yml

### Finally update the deployment in the workspace region so that changes in the workspace bucket are replicated back to source
aws --region eu-west-1 \
cloudformation update-stack \
--stack-name dbs-s3-bidirectional-crr-solution-data \
--capabilities CAPABILITY_NAMED_IAM \
--parameters file://dbs-s3-bidirectional-crr-solution-parameters.json \
--template-body file://dbs-s3-bidirectional-crr-solution.yml

## Example of use

### Populate with raw data the source bucket
aws s3 cp --recursive /Users/ioannis.papadopoulos/Documents/DatabricksDatasets/retail-demo-data \
s3://dbs-ioannis-s3-bidirectional-crr-solution-source-bucket/retail-demo-data

### Mound the bucket and access the data with Databricks
