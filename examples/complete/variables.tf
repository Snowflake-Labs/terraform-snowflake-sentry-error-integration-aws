# Required Variables
variable "prefix" {
  type        = string
  description = "This will be the prefix used to name the Resources."
}

variable "snowflake_account" {
  type      = string
  sensitive = true
}

variable "default_snowflake_error_dsn" {
  description = "Default DSN used to initialize the Sentry SDK in python lambda."
  type        = string
}

variable "jira_cloud_id" {
  description = "ID of your JIRA cloud instance."
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

variable "integration_role" {
  type        = string
  description = "Role for creating database level or account level objects."
  default     = "ACCOUNTADMIN"
}

variable "monitoring_role" {
  type        = string
  description = "Role for creating schema level objects."
  default     = "ACCOUNTADMIN"
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

variable "send_to_sentry_function_user_roles" {
  description = "List of roles to grant usage to send_to_sentry external function."
  type        = list(string)
  default     = []
}

data "aws_caller_identity" "current" {}
data "aws_region" "current" {}
data "aws_partition" "current" {}

locals {
  account_id = data.aws_caller_identity.current.account_id
  aws_region = data.aws_region.current.name
}
