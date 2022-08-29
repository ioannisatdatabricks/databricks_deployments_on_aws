# Deploying a Databricks workspace on an existing VPC

## Description
The dbs-aws-byovpc.yml Cloudformation template creates a Databricks workspace using existing VPC resources.

## Prerequisites
- Having creates the dbs-account-api stack, which exports the functions used for the custom resources

## Example of deploying AWS resources for testing
aws --region eu-west-1 \
cloudformation create-stack \
--stack-name dbs-aws-infra \
--capabilities CAPABILITY_NAMED_IAM \
--template-body file://dbs-aws-infra.yml \
--parameters \
ParameterKey=ResourceOwner,ParameterValue=<RESOURCE_OWNER> \
ParameterKey=DBSRootBucketName,ParameterValue=<ROOT_BUCKET_NAME> \
ParameterKey=DBSVPCCidrBlock,ParameterValue=10.10.0.0/16 \
ParameterKey=DBSNatSubnet1CidrBlock,ParameterValue=10.10.0.0/25 \
ParameterKey=DBSClusterSubnet1CidrBlock,ParameterValue=10.10.4.0/22 \
ParameterKey=DBSClusterSubnet2CidrBlock,ParameterValue=10.10.8.0/22

### Additional parameter for creating a new KMS key
ParameterKey=DBSEncryptionKeyAlias,ParameterValue=databricks-notebook-key \

### Additional parameter for creating an instance profile
ParameterKey=CreateInstanceProfile,ParameterValue=yes \

### Additional parameter for creating a cross-account role for Databricks
ParameterKey=DBSAccountId,ParameterValue=<DATABRICKS_ACCOUNT_ID> \

### Additional parameters for enabling high availability to the internet (it will set up a second NAT in the second availability zone)
ParameterKey=DBSNatSubnet2CidrBlock,ParameterValue=10.10.0.128/25 \

### Additional parameters to prepare additional subnets for PrivateLink:
ParameterKey=DBSPrivateLinkSubnet1CidrBlock,ParameterValue=10.10.2.0/25 \
ParameterKey=DBSPrivateLinkSubnet2CidrBlock,ParameterValue=10.10.2.128/25 \

### Additional parameter to create the PrivateLink VPC endpoints:
ParameterKey=CreatePrivateLinkEndpoints,ParameterValue=yes \

## Example using the AWS CLI to create the workspace using existing AWS resources
aws --region eu-west-1 \
cloudformation create-stack \
--stack-name dbs-aws-byovpc \
--capabilities CAPABILITY_NAMED_IAM \
--template-body file://dbs-aws-byovpc.yml \
--parameters \
ParameterKey=ResourceOwner,ParameterValue=<RESOURCE_OWNER> \
ParameterKey=DBSRootBucket,ParameterValue=<ROOT_BUCKET_NAME> \
ParameterKey=VpcId,ParameterValue=<VPC_ID> \
ParameterKey=ClusterSubnetId1,ParameterValue=<SUBNET_ID_1> \
ParameterKey=ClusterSubnetId2,ParameterValue=<SUBNET_ID_2> \
ParameterKey=WorkspaceSecurityGroupId,ParameterValue=<SECURITY_GROUP_ID> \
ParameterKey=DBSAccountId,ParameterValue=<DATABRICKS_ACCOUNT_ID> \
ParameterKey=DBSUsername,ParameterValue=<DATABRICKS_USER_NAME> \
ParameterKey=DBSPassword,ParameterValue=<DATABRICKS_PASSWORD>

### Additional parameter if the cross-account role already exists
ParameterKey=DBSCrossAccountRoleArn,ParameterValue=<CROSS_ACCOUNT_ROLE_ARN> \

### Additional parameters for using KMS to encrypt the notebooks
ParameterKey=DBSEncryptionKeyArn,ParameterValue=<ENCRYPTION_KEY_ARN> \
### Optional: existing alias for the key (without the "alias/" prefix)
ParameterKey=DBSEncryptionKeyAlias,ParameterValue=<ENCRYPTION_KEY_ALIAS> \

### Additional parameters for enabling Private Link:
ParameterKey=DBSPrivateLinkMode,ParameterValue=PublicAccessEnabled \
ParameterKey=PrivateLinkSubnetId1,ParameterValue=<PRIVATELINK_SUBNET_ID_1> \
ParameterKey=PrivateLinkSubnetId2,ParameterValue=<PRIVATELINK_SUBNET_ID_2> \
ParameterKey=RelayInterfaceEndpointId,ParameterValue=<SCC_RELAY_VPC_ENDPOINT_ID> \
ParameterKey=RestApiInterfaceEndpointId,ParameterValue=<REST_VPC_ENDPOINT_ID> \
