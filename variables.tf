# Required Variables
variable "prefix" {
  type        = string
  description = "This will be the prefix used to name the Resources."
}

variable "default_snowflake_error_dsn" {
  description = "Default DSN used to initialize the Sentry SDK in python lambda."
  type        = string
}

# Optional Variables
variable "aws_region" {
  description = "The AWS region in which the AWS infrastructure is created."
  type        = string
  default     = "us-west-2"
}

variable "aws_cloudwatch_metric_namespace" {
  type        = string
  description = "cloudwatch prefix for lambda metrics."
  default     = "*"
}

variable "log_retention_days" {
  description = "Log retention period in days."
  default     = 0 # Forever
}

variable "env" {
  type        = string
  description = "Dev/Prod/Staging or any other custom environment name."
  default     = "dev"
}

variable "snowflake_integration_user_roles" {
  type = list(string)
  default = [
    "SECURITY_MONITORING_RL"
  ]
  description = "List of roles to which Sentry infra will GRANT USAGE ON INTEGRATION perms."
}

variable "deploy_lambda_in_vpc" {
  type        = bool
  description = "The SG VPC ID for the Lambda function."
  default     = false
}

variable "lambda_security_group_ids" {
  type        = list(string)
  default     = []
  description = "The SG IDs for the lambda function."
}

variable "lambda_subnet_ids" {
  type        = list(string)
  default     = []
  description = "The subnet IDs for the lambda function."
}

variable "vpc_id" {
  type        = string
  description = "The VPC ID for creating the lambda and security group ID."
  default     = null
}

variable "arn_format" {
  type        = string
  description = "ARN format could be aws or aws-us-gov. Defaults to non-gov."
  default     = "aws"
}

variable "database" {
  type        = string
  description = "Snowflake Database in which the snowflake db level objects are created."
  default     = "SNOWALERT"
}

variable "monitoring_schema" {
  type        = string
  description = "Snowflake Schema in which the snowflake db schema level objects are created."
  default     = "MONITORING"
}

variable "warehouse" {
  type        = string
  description = "Snowflake Warehouse used for any compute such as tasks and external functions."
  default     = "SNOWALERT_WAREHOUSE"
}

variable "slack_secrets_arn" {
  description = "The ARN for the secrets user by the sentry slack app."
  type        = string
}

variable "jira_secrets_arn" {
  description = "The ARN for the secrets user by the sentry slack app."
  type        = string
}

variable "sentry_hostname" {
  description = "Hostname of the Sentry instance."
  type        = string
}


data "aws_caller_identity" "current" {}
data "aws_region" "current" {}
data "aws_partition" "current" {}


locals {
  account_id = data.aws_caller_identity.current.account_id
  aws_region = data.aws_region.current.name
}

locals {
  inferred_api_gw_invoke_url = "https://${aws_api_gateway_rest_api.ef_to_lambda.id}.execute-api.${local.aws_region}.amazonaws.com/"
  sentry_integration_prefix  = "${var.prefix}-sentry-integration"
}

locals {
  lambda_function_name             = "${local.sentry_integration_prefix}-lambda"
  lambda_backtraffic_function_name = "${var.prefix}-sentry-backtraffic-lambda"
  api_gw_caller_role_name          = "${local.sentry_integration_prefix}-api-gateway-caller"
  api_gw_logger_role_name          = "${local.sentry_integration_prefix}-api-gateway-logger"

  sentry_sns_role_name   = "${local.sentry_integration_prefix}-sns"
  sentry_sns_policy_name = "${local.sentry_integration_prefix}-sns-policy"
  sentry_sns_topic_name  = "${local.sentry_integration_prefix}-sns-topic"
}
