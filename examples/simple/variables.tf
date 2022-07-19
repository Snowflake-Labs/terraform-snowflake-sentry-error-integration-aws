# Required Variables
variable "prefix" {
  type        = string
  description = "This will be the prefix used to name the Resources."
}

variable "snowflake_account" {
  type      = string
  sensitive = true
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

variable "security_integration_role" {
  type        = string
  description = "Role for creating database level or account level objects."
  default     = "ACCOUNTADMIN"
}

variable "security_monitoring_role" {
  type        = string
  description = "Role for creating schema level objects."
  default     = "ACCOUNTADMIN"
}

variable "database_name" {
  type        = string
  description = "Database where the EF and tasks are created."
  default     = "SNOWALERT"
}

variable "schema_name" {
  type        = string
  description = "Schema where the EF and tasks are created."
  default     = "MONITORING"
}

data "aws_caller_identity" "current" {}
data "aws_region" "current" {}
data "aws_partition" "current" {}


locals {
  account_id = data.aws_caller_identity.current.account_id
  aws_region = data.aws_region.current.name
}
