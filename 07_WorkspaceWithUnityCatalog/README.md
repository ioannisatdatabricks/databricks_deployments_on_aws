# Workspace creation with Unity Catalog Metastore

## Description
The dbs-workspace-with-uc.yml Cloudformation template creates all the required resources on AWS for setting up a Unity Catalog-enabled workspace

## Prerequisites
- Having creates the dbs-account-api stack, which exports the functions used for the custom resources

## Example of deploying a Unity Catalog metastore
When the UCMetastoreDefaultStorageBucketName is specified then a new metastore is created, otherwise an existing one in the same region is used. Delta Sharing is enabled if the DeltaSharingTokenLifetimeSeconds is specified.

aws --region <AWS_REGION> \
cloudformation create-stack \
--stack-name <STACK_NAME> \
--capabilities CAPABILITY_NAMED_IAM \
--template-body file://dbs-workspace-with-uc.yml \
--parameters \
ParameterKey=ResourceOwner,ParameterValue=<RESOURCE_OWNER> \
ParameterKey=DBSAccountId,ParameterValue=<DATABRICKS_ACCOUNT_ID> \
ParameterKey=DBSUsername,ParameterValue=<DATABRICKS_USER_NAME> \
ParameterKey=DBSPassword,ParameterValue=<DATABRICKS_PASSWORD> \
ParameterKey=DBFSRootBucketName,ParameterValue=<DBFS_ROOT_BUCKET_NAME> \
ParameterKey=UCMetastoreDefaultStorageBucketName,ParameterValue=<METASTORE_BUCKET_NAME> \
ParameterKey=DeltaSharingTokenLifetimeSeconds,ParameterValue=<DS_TOKEN_LIFETIME_SECONDS> \
ParameterKey=DeltaSharingOrgName,ParameterValue=<DS_ORG_NAME>
