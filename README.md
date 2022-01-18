# AWS Deployment Architectures

## Cloudformation custom resources to wrap the Databricks API
The folder 00_DBSAccountAPIFunctions contains a Cloudformation template the definition of lammbda functions which wrap the Databricks Account API, as well as instructions of how to run it.
The functions are exported in Cloudformation to allow "custom resources" to be created in dependent stacks.

## Baseline architecture
The folder 01_BaselineArchitecture contains a Cloudformation template which:
- Creates all the resources in an AWS account (S3 root bucket, VPC and resources therein, an EC2 instance profile and a cross-account IAM role) needed for an AWS deployment
- Creates the relevant configuration objects in a Databricks account as well as a workspace.

## Bring Your Own VPC
The folder 04_BringYourOwnVpc contains instructions and a Cloudformation template that demonstrates how to deploy a Databricks workspace in an existing VPC.

## Setting up a cross-region replicated S3 bucket
The folder 02_CrossRegionReplicatedBucket contains instructions, scripts and a Cloudformation template in order to create two S3 buckets in different regions, which are cross-replicated, in order to accommodate the use case of a customer with data in a region where the Databricks E2 deployment is not available

## Accessing a remote S3 bucket using VPC peering
The folder 03_VpcPeering contains instructions, scripts and a Cloudformation template that demonstrates how one can access through Databricks an S3 bucket which is located in a remote region by using VPC peering.
