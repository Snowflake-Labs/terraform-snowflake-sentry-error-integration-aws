resource "snowflake_notification_integration" "pipe_errors_integration" {
  provider = snowflake.notification_integration_role

  name    = "${upper(replace(var.prefix, "-", "_"))}_NOTIFICATION_INTEGRATION"
  comment = "A notification integration."

  enabled   = true
  type      = "QUEUE"
  direction = "OUTBOUND"

  # AWS_SNS
  notification_provider = "AWS_SNS"
  aws_sns_topic_arn     = aws_sns_topic.sentry_integration_sns.arn
  aws_sns_role_arn      = "arn:${var.arn_format}:iam::${local.account_id}:role/${local.sentry_sns_role_name}"
}

resource "snowflake_integration_grant" "sentry_integration_notification_integration_grant" {
  provider = snowflake.notification_integration_role

  integration_name  = snowflake_notification_integration.pipe_errors_integration.name
  privilege         = "USAGE"
  roles             = var.snowflake_integration_user_roles
  with_grant_option = false
}
