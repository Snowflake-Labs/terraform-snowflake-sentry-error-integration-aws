# This file contains the following IAM resources:
# 1. Role  and Policy attachment for the role that the api gateway will assume.
# 2. Role, Role Policy and Policy attachment for the role that the external function will assume.
# 3. Lambda Assume Role, Assume Role Policy and other Permissions Policy.

# ----------------------------------------------------------------------------
# 1. Role and Policy attachment for the role that the api gateway will assume.
# ----------------------------------------------------------------------------
data "aws_iam_policy_document" "sentry_integration_api_gateway_assume_role_policy_doc" {
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["apigateway.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "sentry_integration_api_gateway_assume_role" {
  name               = local.api_gw_logger_role_name
  assume_role_policy = data.aws_iam_policy_document.sentry_integration_api_gateway_assume_role_policy_doc.json
}

resource "aws_iam_role_policy_attachment" "gateway_logger_policy_attachment" {
  role       = aws_iam_role.sentry_integration_api_gateway_assume_role.id
  policy_arn = "arn:${var.arn_format}:iam::aws:policy/service-role/AmazonAPIGatewayPushToCloudWatchLogs"
}

resource "aws_api_gateway_account" "api_gateway" {
  cloudwatch_role_arn = aws_iam_role.sentry_integration_api_gateway_assume_role.arn
}

# -----------------------------------------------------------------------------------------------
# 2. Role, Role Policy and Policy attachment for the role that the external function will assume.
# -----------------------------------------------------------------------------------------------
resource "aws_iam_role" "gateway_caller" {
  name = local.api_gw_caller_role_name
  path = "/"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Condition = {
          StringEquals = {
            "sts:ExternalId" = snowflake_api_integration.sentry_integration_api_integration.api_aws_external_id
          }
        }
        Effect = "Allow"
        Principal = {
          AWS = snowflake_api_integration.sentry_integration_api_integration.api_aws_iam_user_arn
        }
      }
    ]
  })
}

resource "aws_iam_role_policy" "gateway_caller_policy" {
  name = "${local.sentry_integration_prefix}-invoke-api-gateway-policy"
  role = aws_iam_role.gateway_caller.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = "execute-api:Invoke"
        Resource = "${aws_api_gateway_rest_api.ef_to_lambda.execution_arn}/*/*/*"
      }
    ]
  })
}

# -----------------------------------------------------------------------
# 3. Lambda Assume Role, Assume Role Policy and other Permissions Policy.
# -----------------------------------------------------------------------
data "aws_iam_policy_document" "sentry_integration_lambda_assume_role_policy_doc" {
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "sentry_integration_lambda_assume_role" {
  name               = "${local.sentry_integration_prefix}-lambda"
  assume_role_policy = data.aws_iam_policy_document.sentry_integration_lambda_assume_role_policy_doc.json
}

data "aws_iam_policy_document" "sentry_integration_lambda_policy_doc" {
  # Write logs to cloudwatch
  statement {
    sid    = "WriteCloudWatchLogs"
    effect = "Allow"
    resources = [
      "arn:${var.arn_format}:logs:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:log-group:/aws/lambda/${local.lambda_function_name}:*"
    ]

    actions = [
      "logs:CreateLogStream",
      "logs:PutLogEvents",
    ]
  }

  statement {
    sid       = "EcrScanImages"
    effect    = "Allow"
    resources = ["*"]

    actions = [
      "ecr:DescribeRepositories",
      "ecr:ListImages",
      "ecr:DescribeImages",
      "ecr:BatchGetImage",
      "ecr:DescribeImageScanFindings",
      "ecr:StartImageScan",
    ]
  }

  # Access to secrets needed by lambda
  statement {
    sid       = "ListSecrets"
    effect    = "Allow"
    resources = ["*"]
    actions   = ["secretsmanager:ListSecrets"]
  }
}

resource "aws_iam_role_policy" "sentry_integration_lambda_policy" {
  name   = "${local.sentry_integration_prefix}-lambda-policy"
  role   = aws_iam_role.sentry_integration_lambda_assume_role.id
  policy = data.aws_iam_policy_document.sentry_integration_lambda_policy_doc.json
}

resource "aws_iam_role_policy_attachment" "sentry_integration_lambda_vpc_policy_attachment" {
  count = var.deploy_lambda_in_vpc ? 1 : 0

  role       = aws_iam_role.sentry_backtraffic_proxy_lambda_role.name
  policy_arn = "arn:${var.arn_format}:iam::aws:policy/service-role/AWSLambdaENIManagementAccess"
}

# -----------------------------------------------------------------------------------------------
# 4. Role, Role Policy and Policy attachment for the role that the external function will assume.
# -----------------------------------------------------------------------------------------------
resource "aws_iam_role" "sentry_sns_role" {
  name = local.sentry_sns_role_name
  path = "/"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Condition = {
          StringEquals = {
            "sts:ExternalId" = snowflake_notification_integration.pipe_errors_integration.aws_sns_external_id
          }
        }
        Effect = "Allow"
        Principal = {
          AWS = snowflake_notification_integration.pipe_errors_integration.aws_sns_iam_user_arn
        }
      }
    ]
  })
}

resource "aws_iam_role_policy" "sentry_sns_role_policy" {
  name = local.sentry_sns_policy_name
  role = aws_iam_role.sentry_sns_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = "sns:Publish"
        Resource = aws_sns_topic.sentry_integration_sns.arn
      }
    ]
  })
}

# -------------------------------------------------
# 5. SNS Topic Policy, SNS Topic Policy Attachment.
# -------------------------------------------------
data "aws_iam_policy_document" "sentry_integration_sns_topic_policy_doc" {
  policy_id = local.sentry_sns_policy_name

  statement {
    sid       = "SNSPublish"
    effect    = "Allow"
    resources = [aws_sns_topic.sentry_integration_sns.arn]
    actions   = ["SNS:Publish"]

    principals {
      type        = "AWS"
      identifiers = ["*"]
    }

  }

  statement {
    sid       = "SNSSubscribe"
    effect    = "Allow"
    resources = [aws_sns_topic.sentry_integration_sns.arn]
    actions   = ["sns:Subscribe"]

    principals {
      type        = "AWS"
      identifiers = ["*"]
    }
  }
}

resource "aws_sns_topic_policy" "sentry_integration_sns_topic_policy" {
  arn    = aws_sns_topic.sentry_integration_sns.arn
  policy = data.aws_iam_policy_document.sentry_integration_sns_topic_policy_doc.json
}

# -----------------------------------------------------------------------------------
# 6. Backtraffic Lambda Assume Role, Assume Role Policy and other Permissions Policy.
# -----------------------------------------------------------------------------------
data "aws_iam_policy_document" "sentry_backtraffic_proxy_lambda_role_policy_doc" {
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "sentry_backtraffic_proxy_lambda_role" {
  name               = "${local.lambda_backtraffic_function_name}-role"
  assume_role_policy = data.aws_iam_policy_document.sentry_backtraffic_proxy_lambda_role_policy_doc.json
}

data "aws_iam_policy_document" "sentry_backtraffic_proxy_lambda_policy_doc" {
  # Write logs to cloudwatch
  statement {
    sid       = "WriteCloudWatchLogs"
    effect    = "Allow"
    resources = ["arn:${var.arn_format}:logs:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:log-group:/aws/lambda/${local.lambda_backtraffic_function_name}:*"]

    actions = [
      "logs:CreateLogStream",
      "logs:PutLogEvents",
    ]
  }

  statement {
    sid       = "AccessGetSecretVersions"
    effect    = "Allow"
    resources = local.backtraffic_lambda_secrets_arns
    actions = [
      "secretsmanager:GetResourcePolicy",
      "secretsmanager:GetSecretValue",
      "secretsmanager:DescribeSecret",
      "secretsmanager:ListSecretVersionIds",
      "secretsmanager:ListSecrets"
    ]
  }

  statement {
    sid       = "ListSecrets"
    effect    = "Allow"
    resources = ["*"]
    actions = [
      "secretsmanager:ListSecrets"
    ]
  }
}

resource "aws_iam_role_policy" "sentry_backtraffic_proxy_lambda_policy" {
  name   = "${local.lambda_backtraffic_function_name}-role-policy"
  role   = aws_iam_role.sentry_backtraffic_proxy_lambda_role.id
  policy = data.aws_iam_policy_document.sentry_backtraffic_proxy_lambda_policy_doc.json
}

resource "aws_iam_role_policy_attachment" "sentry_backtraffic_proxy_lambda_vpc_policy_attachment" {
  count = var.deploy_lambda_in_vpc ? 1 : 0

  role       = aws_iam_role.sentry_backtraffic_proxy_lambda_role.name
  policy_arn = "arn:${var.arn_format}:iam::aws:policy/service-role/AWSLambdaENIManagementAccess"
}
