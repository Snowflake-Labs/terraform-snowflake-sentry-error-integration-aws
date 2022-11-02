output "api_gateway_invoke_url" {
  description = "This is the inferred API Gateway invoke URL which we use as allowed prefixes."
  value       = aws_api_gateway_deployment.sentry_integration_api_gw_deployment.invoke_url
}

output "api_integration_name" {
  description = "Name of API integration"
  value       = snowflake_api_integration.sentry_integration_api_integration.name
}

output "notification_integration_name" {
  description = "Name of Storage integration"
  value       = module.sentry_error_integration.notification_integration_name
}

output "notification_integration_sns_topic_arn" {
  description = "Name of Storage integration"
  value       = module.sentry_error_integration.notification_integration_sns_topic_arn
}

output "notification_integration_sns_role_arn" {
  description = "Name of Storage integration"
  value       = module.sentry_error_integration.notification_integration_sns_role_arn
}

output "sns_topic_arn" {
  description = "Sentry SNS topic."
  value       = aws_sns_topic.sentry_integration_sns.arn
}

output "sentry_integration_lambda_sg_ids" {
  description = "Lambda SG IDs."
  value       = var.deploy_lambda_in_vpc && length(var.lambda_security_group_ids) == 0 ? [aws_security_group.sentry_integration_lambda_sg.0.id] : var.lambda_security_group_ids
}

output "sentry_integration_sns_iam_role" {
  description = "SNS IAM Role ARN."
  value       = aws_iam_role.sentry_sns_role.arn
}

output "send_to_sentry_full_function_name" {
  description = "Fully qualified function name with database and schema."
  value = join(".", [
    var.database,
    var.monitoring_schema,
    snowflake_external_function.send_to_sentry.name,
  ])
}

output "sentry_backtraffic_api_gateway_url" {
  description = "API Gateway URL to use for 3rdparty serives that need to access Sentry webhooks."
  value       = module.sentry_backtraffic_api_gateway.apigatewayv2_api_api_endpoint
}
