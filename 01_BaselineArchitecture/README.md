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
ParameterKey=DBSNatSubnet1CidrBlock,ParameterValue=10.10.0.0/25 \
ParameterKey=DBSClusterSubnet1CidrBlock,ParameterValue=10.10.4.0/22 \
ParameterKey=DBSClusterSubnet2CidrBlock,ParameterValue=10.10.8.0/22 \
ParameterKey=DBSEncryptionKeyAlias,ParameterValue=databricks-notebook-key \
ParameterKey=DBSInstanceProfileRoleName,ParameterValue=DatabricksInstanceProfileRole \
ParameterKey=DBSCrossAccountRoleName,ParameterValue=DatabricksCrossAccountRole \
ParameterKey=DBSAccountId,ParameterValue=<DATABRICKS_ACCOUNT_ID> \
ParameterKey=DBSUsername,ParameterValue=<DATABRICKS_USER_NAME> \
ParameterKey=DBSPassword,ParameterValue=<DATABRICKS_PASSWORD>

### Additional parameters for enabling the network firewall
ParameterKey=DBSFirewallSubnet1CidrBlock,ParameterValue=10.10.1.0/25 \

### Additional parameters for enabling Private Link:
ParameterKey=DBSPrivateLinkMode,ParameterValue=PublicAccessEnabled \
ParameterKey=DBSPrivateLinkSubnet1CidrBlock,ParameterValue=10.10.2.0/25 \
ParameterKey=DBSPrivateLinkSubnet2CidrBlock,ParameterValue=10.10.2.128/25 \

### Additional parameters for enabling high availability to the internet (it will set up a second NAT in the second availability zone)
ParameterKey=DBSNatSubnet2CidrBlock,ParameterValue=10.10.0.128/25 \
#### If a firewall is enabled then this one needs to be set up as well:
ParameterKey=DBSFirewallSubnet2CidrBlock,ParameterValue=10.10.1.128/25 \


## Testing connectivity to a PrivateLink-enabled workspace with public access disabled.

### Set up private DNS
- Create a private hosted zone for cloud.databricks.com
- Associate the VPC to the private hosted zone
- Create an alias A record for the workspace URL targeting the PrivateLink workspace VPC endpoint.

### Set up SSH tunneling
- Create an EC2 RSA key for ssh connectivity
- Create a security group allowing incoming connections to port 22 (SSH)
- Launch a micro instance on EC2 on the public subnet (where the NAT Gateway is attached to)specifying the two security groups (the one with the SSH connectivity and the one used for the clusters and the VPC endpoints)
- From the local machine run ssh -N -i <key>.pem -D 9090 ec2-user@<EC2_PUBLIC_DNS_NAME>

### Configure SOCKS on Firefox and access the workspace
- In the upper right-hand corner, click on the hamburger icon ☰ to open Firefox’s menu:
- Click on the ⚙ Preferences link.
- Scroll down to the Network Settings section and click on the Settings... button.
- Select the Manual proxy configuration radio button.
- Enter 127.0.0.1 in the SOCKS Host field and 9090 in the Port field.
- Check the Proxy DNS when using SOCKS v5 checkbox.
- Click on the OK button to save the settings.
- Type the workspace URL to access it.
