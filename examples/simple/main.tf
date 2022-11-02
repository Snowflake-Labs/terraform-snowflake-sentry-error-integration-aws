module "sentry_integration" {
  source = "../../"

  # General
  prefix = var.prefix
  env    = var.env

  # AWS
  arn_format                      = var.arn_format
  aws_cloudwatch_metric_namespace = var.aws_cloudwatch_metric_namespace
  aws_region                      = var.aws_region

  deploy_lambda_in_vpc      = var.deploy_lambda_in_vpc
  lambda_security_group_ids = var.lambda_security_group_ids
  lambda_subnet_ids         = var.lambda_subnet_ids
  vpc_id                    = var.vpc_id

  database                         = var.database
  monitoring_schema                = var.monitoring_schema
  warehouse                        = var.warehouse
  snowflake_integration_user_roles = var.snowflake_integration_user_roles

  default_snowflake_error_dsn = var.default_snowflake_error_dsn
  sentry_hostname             = var.sentry_hostname
  jira_secrets_arn            = var.jira_secrets_arn
  slack_secrets_arn           = var.slack_secrets_arn

  providers = {
    snowflake.api_integration_role          = snowflake.api_integration_role
    snowflake.notification_integration_role = snowflake.notification_integration_role
    snowflake.monitoring_role               = snowflake.monitoring_role
    aws                                     = aws
  }
}
