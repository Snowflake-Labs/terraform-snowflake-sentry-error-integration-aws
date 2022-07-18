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

  snowflake_integration_user_roles = var.snowflake_integration_user_roles

  providers = {
    snowflake.api_integration_role          = snowflake.api_integration_role
    snowflake.notification_integration_role = snowflake.notification_integration_role
    aws                                     = aws
  }
}
