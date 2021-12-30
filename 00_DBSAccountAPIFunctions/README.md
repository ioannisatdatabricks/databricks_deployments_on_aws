# Databricks API wrappers

The dbs-account-api.yml Cloudformation template defines Lambda functions wrapping Databricks API calls to be used for custom Cloudformation resources.

## Example using the AWS CLI
aws --region eu-west-1 \
cloudformation create-stack \
--stack-name dbs-account-api \
--capabilities CAPABILITY_NAMED_IAM \
--parameters \
ParameterKey=ResourceOwner,ParameterValue=<RESOURCE_OWNER> \
ParameterKey=ResourcePrefix,ParameterValue=DatabricksAccountAPI \
--template-body file://dbs-account-api.yml

## TODO
- Support update operations for the workspace object
- Implement functions to support PrivateLink related custom resources