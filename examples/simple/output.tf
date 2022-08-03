output "api_gateway_invoke_url" {
  description = "This is the inferred API Gateway invoke URL which we use as allowed prefixes."
  value       = module.sentry_integration.api_gateway_invoke_url
}

output "api_integration_name" {
  description = "Name of API integration"
  value       = module.sentry_integration.api_integration_name
}

output "notification_integration_name" {
  description = "Name of Storage integration"
  value       = module.sentry_integration.notification_integration_name
}

output "sns_topic_arn" {
  description = "Sentry SNS topic."
  value       = module.sentry_integration.sns_topic_arn
}

output "sentry_integration_lambda_sg_ids" {
  description = "Lambda SG IDs."
  value       = module.sentry_integration.sentry_integration_lambda_sg_ids
}

output "sentry_integration_sns_iam_role" {
  description = "SNS IAM Role ARN."
  value       = module.sentry_integration.sentry_integration_sns_iam_role
}

output "sentry_integration_sns_iam_role" {
  description = "SNS IAM Role ARN."
  value       = module.sentry_integration.sentry_integration_sns_iam_role
}

output "sentry_backtraffic_api_gateway_url" {
  description = "API Gateway URL to use for 3rdparty serives that need to access Sentry webhooks."
  value       = module.sentry_backtraffic_api_gateway.apigatewayv2_api_api_endpoint
}
