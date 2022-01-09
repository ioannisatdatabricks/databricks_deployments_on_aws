# Baseline Architecture and deployment on AWS and Databricks

## Description
The dbs-aws-baseline.yml Cloudformation template creates all the required resources on AWS for a Databricks deployment. It is also creating a Databricks workspace using custom resources.

The template can be modified so that if some resources are already existing (Root bucket, VPC, KMS keys, etc), then they can be passed as parameters for the downstream ones.

## Prerequisites
- Having creates the dbs-account-api stack, which exports the functions used for the custom resources

## Example using the AWS CLI to create all resources
aws --region eu-west-1 \
cloudformation create-stack \
--stack-name dbs-aws-baseline \
--capabilities CAPABILITY_NAMED_IAM \
--template-body file://dbs-aws-baseline.yml \
--parameters \
ParameterKey=ResourceOwner,ParameterValue=<RESOURCE_OWNER> \
ParameterKey=DBSRootBucketName,ParameterValue=<ROOT_BUCKET_NAME> \
ParameterKey=DBSVPCCidrBlock,ParameterValue=10.10.0.0/16 \
ParameterKey=DBSPublicSubnet1CidrBlock,ParameterValue=10.10.0.0/24 \
ParameterKey=DBSPrivateSubnet1CidrBlock,ParameterValue=10.10.4.0/22 \
ParameterKey=DBSPrivateSubnet2CidrBlock,ParameterValue=10.10.8.0/22 \
ParameterKey=DBSEncryptionKeyAlias,ParameterValue=databricks-notebook-key \
ParameterKey=DBSInstanceProfileRoleName,ParameterValue=DatabricksInstanceProfileRole \
ParameterKey=DBSCrossAccountRoleName,ParameterValue=DatabricksCrossAccountRole \
ParameterKey=DBSAccountId,ParameterValue=<DATABRICKS_ACCOUNT_ID> \
ParameterKey=DBSUsername,ParameterValue=<DATABRICKS_USER_NAME> \
ParameterKey=DBSPassword,ParameterValue=<DATABRICKS_PASSWORD>

### Additional parameters for enabling Private Link:
ParameterKey=DBSPrivateLinkMode,ParameterValue=PublicAccessEnabled \
ParameterKey=DBSPrivateLinkSubnet1CidrBlock,ParameterValue=10.10.2.0/24 \
ParameterKey=DBSPrivateLinkSubnet2CidrBlock,ParameterValue=10.10.3.0/24 \

### Additional parameters for enabling high availability to the internet (it will set up a second NAT in the second availability zone)
ParameterKey=DBSPublicSubnet2CidrBlock,ParameterValue=10.10.1.0/24 \
