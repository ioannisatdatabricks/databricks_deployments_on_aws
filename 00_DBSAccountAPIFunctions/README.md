# Databricks API wrappers

The dbs-account-api.yml Cloudformation template defines Lambda functions wrapping Databricks API calls to be used for custom Cloudformation resources.

## Example using the AWS CLI
aws --region <AWS_REGION> \
cloudformation create-stack \
--stack-name dbs-account-api \
--capabilities CAPABILITY_NAMED_IAM \
--parameters \
ParameterKey=ResourceOwner,ParameterValue=<RESOURCE_OWNER> \
--template-body file://dbs-account-api.yml

## Examples of calling the custom resouces
The exampleCustomResources.yml template provides an example of how the relevant custom resources may be created in a CloudFormation script

## TODO
Make the workspace creation and update idempotent so that it can be protected against repeated CloudFormation calls