module "sentry_error_integration" {
  source = "Snowflake-Labs/notification-integration-aws/snowflake"

  prefix                           = "${var.prefix}-sentry"
  aws_region                       = var.aws_region
  env                              = var.env
  snowflake_integration_user_roles = var.snowflake_integration_user_roles
  arn_format                       = var.arn_format

  providers = {
    snowflake.notification_integration_role = snowflake.notification_integration_role
    aws                                     = aws
  }
}
