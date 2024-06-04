module "sentry_backtraffic_api_gateway" {
  source  = "terraform-aws-modules/apigateway-v2/aws"
  version = "4.0.0"

  name          = "${local.sentry_integration_prefix}-backtraffic"
  description   = "HTTPS API Gateway for slack to tines traffic."
  protocol_type = "HTTP"

  create_api_domain_name                   = false
  default_stage_access_log_destination_arn = aws_cloudwatch_log_group.api_gw_sentry_backtraffic_log_group.arn
  default_stage_access_log_format          = "$context.identity.sourceIp - - [$context.requestTime] \"$context.httpMethod $context.routeKey $context.protocol\" $context.status $context.responseLength $context.requestId $context.integrationErrorMessage"

  default_route_settings = {
    detailed_metrics_enabled = true
    throttling_burst_limit   = 5000
    throttling_rate_limit    = 10000
    # logging_level            = "INFO" -- Supported only for WebSocket APIs
    # data_trace_enabled       = true   -- Supported only for WebSocket APIs
  }

  integrations = {
    "ANY /{proxy+}" = {
      lambda_arn             = aws_lambda_function.sentry_backtraffic_proxy_lambda.invoke_arn
      payload_format_version = "2.0"
      timeout_milliseconds   = 12000
      connection_type        = "INTERNET"
      integration_method     = "POST"
      passthrough_behavior   = "WHEN_NO_MATCH"
      integration_type       = "AWS_PROXY"
    }
  }
}

resource "aws_lambda_permission" "allow_api_gw" {
  statement_id  = "AllowAPIgatewayInvokation"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.sentry_backtraffic_proxy_lambda.function_name
  principal     = "apigateway.amazonaws.com"
}
