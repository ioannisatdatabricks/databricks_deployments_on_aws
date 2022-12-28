# Unity Catalog Metastore Setting Up

## Description
The uc-metastore.yml Cloudformation template creates all the required resources on AWS for setting up a Unity Catalog metastore, and the actual metastore in a Databricks account.

## Prerequisites
- Having creates the dbs-account-api stack, which exports the functions used for the custom resources

## Example of deploying a Unity Catalog metastore

aws --region <AWS+REGION> \
cloudformation create-stack \
--stack-name <STACK_NAME> \
--capabilities CAPABILITY_NAMED_IAM \
--template-body file://uc-metastore.yml \
--parameters \
ParameterKey=ResourceOwner,ParameterValue=<RESOURCE_OWNER> \
ParameterKey=DBSAccountId,ParameterValue=<DATABRICKS_ACCOUNT_ID> \
ParameterKey=DBSUsername,ParameterValue=<DATABRICKS_USER_NAME> \
ParameterKey=DBSPassword,ParameterValue=<DATABRICKS_PASSWORD> \
ParameterKey=UCMetastoreDefaultStorageBucketName,ParameterValue=<METASTORE_BUCKET_NAME> \
ParameterKey=StorageCredentialsIAMRoleName,ParameterValue=<METASTORE_CREDENTIAL_ROLE> \
ParameterKey=DeltaSharingTokenLifetimeSeconds,ParameterValue=<DS_TOKEN_LIFETIME_SECONDS> \
ParameterKey=DeltaSharingOrgName,ParameterValue=<DS_ORG_NAME>
