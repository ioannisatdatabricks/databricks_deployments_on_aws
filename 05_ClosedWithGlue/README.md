# Deploying a Databricks workspace in a VPC without internet access, using Glue as a metastore

## Description
The dbs-aws-closed-with-glue.yml Cloudformation template creates a Databricks workspace in a VPC which does not have access to the public internet.
To this end PrivateLink is enabled and Glue is used for the metastore.

## Prerequisites
- Having creates the dbs-account-api stack, which exports the functions used for the custom resources

## Example of deploying AWS resources for testing
aws --region eu-west-1 \
cloudformation create-stack \
--stack-name dbs-aws-closed-with-glue \
--capabilities CAPABILITY_NAMED_IAM \
--template-body file://dbs-aws-closed-with-glue.yml \
--parameters \
ParameterKey=ResourceOwner,ParameterValue=<RESOURCE_OWNER> \
ParameterKey=DBSRootBucketName,ParameterValue=<ROOT_BUCKET_NAME> \
ParameterKey=DBSVPCCidrBlock,ParameterValue=10.10.0.0/16 \
ParameterKey=DBSClusterSubnet1CidrBlock,ParameterValue=10.10.4.0/22 \
ParameterKey=DBSClusterSubnet2CidrBlock,ParameterValue=10.10.8.0/22 \
ParameterKey=DBSPrivateLinkSubnet1CidrBlock,ParameterValue=10.10.2.0/25 \
ParameterKey=DBSPrivateLinkSubnet2CidrBlock,ParameterValue=10.10.2.128/25 \
ParameterKey=DBSPrivateLinkMode,ParameterValue=PublicAccessEnabled \
ParameterKey=DBSAccountId,ParameterValue=<DATABRICKS_ACCOUNT_ID> \
ParameterKey=DBSUsername,ParameterValue=<DATABRICKS_USER_NAME> \
ParameterKey=DBSPassword,ParameterValue=<DATABRICKS_PASSWORD>

### Use of a existing instance profile
ParameterKey=DBSInstanceProfileArn,ParameterValue=<INSTANCE_PROFILE_ROLE_ARN> \

### Use of existing cross-account role
ParameterKey=DBSCrossAccountRoleArn,ParameterValue=<CROSS_ACCOUNT_ROLE_ARN> \

### Additional parameters for using KMS to encrypt the notebooks
ParameterKey=DBSEncryptionKeyArn,ParameterValue=<ENCRYPTION_KEY_ARN> \

### Optional: existing alias for the key (without the "alias/" prefix)
ParameterKey=DBSEncryptionKeyAlias,ParameterValue=<ENCRYPTION_KEY_ALIAS> \

## Cluster configuration
Use the instance profile

### Spark configuration
spark.databricks.hive.metastore.glueCatalog.enabled true
spark.sql.legacy.createHiveTableByDefault false

### Environment variables
REGION=eu-west-1