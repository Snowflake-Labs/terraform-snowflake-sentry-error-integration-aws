resource "aws_cloudwatch_log_group" "sentry_integration_lambda_log_group" {
  name              = "/aws/lambda/${local.lambda_function_name}"
  retention_in_days = var.log_retention_days

  tags = {
    name = "${local.sentry_integration_prefix}"
  }
}

resource "aws_cloudwatch_log_group" "sentry_integration_api_gateway_log_group" {
  # We can't change this log group name, as it is fixed by AWS.
  # https://github.com/hashicorp/terraform-provider-aws/issues/8413
  name              = "API-Gateway-Execution-Logs_${aws_api_gateway_rest_api.ef_to_lambda.id}/${var.env}"
  retention_in_days = var.log_retention_days

  tags = {
    name = "${local.sentry_integration_prefix}-api-gateway"
  }
}

resource "aws_cloudwatch_log_group" "sentry_backtraffic_proxy_lambda_log_group" {
  name              = "/aws/lambda/${local.lambda_backtraffic_function_name}"
  retention_in_days = var.log_retention_days

  tags = {
    name = "${local.sentry_integration_prefix}-backtraffic-lambda"
  }
}

resource "aws_cloudwatch_log_group" "api_gw_sentry_backtraffic_log_group" {
  name = "/aws/api-gateway-${var.env}/${local.sentry_integration_prefix}-backtraffic-api-gw"
}
