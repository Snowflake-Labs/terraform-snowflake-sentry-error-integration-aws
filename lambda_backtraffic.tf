locals {
  source_code_path_backtraffic          = "lambda-code-backtraffic"
  output_dist_file_name_backtraffic     = "lambda-code-backtraffic.zip"
  runtime_backtraffic                   = "python3.9"
  source_code_dist_dir_name_backtraffic = "lambda-code-dist-backtraffic"
}

resource "null_resource" "install_python_dependencies_backtraffic" {
  # If this always runs archive_file is fine, else we have an issue during refresh:
  # https://github.com/hashicorp/terraform-provider-archive/issues/78
  triggers = {
    always_run = timestamp()
  }

  provisioner "local-exec" {
    command = "bash ${path.module}/scripts/create_dist_pkg_backtraffic.sh"

    environment = {
      source_code_path          = local.source_code_path_backtraffic
      source_code_dist_dir_name = local.source_code_dist_dir_name_backtraffic
      runtime                   = local.runtime_backtraffic
      path_module               = path.module
      path_cwd                  = path.cwd
    }
  }
}

data "archive_file" "lambda_code_back_traffic" {
  source_dir  = "${path.module}/${local.source_code_dist_dir_name_backtraffic}/"
  output_path = "${path.module}/${local.output_dist_file_name_backtraffic}"

  type = "zip"
  excludes = [
    "__pycache__",
    ".mypy_cache",
    ".pytest_cache",
    "venv",
  ]

  depends_on = [null_resource.install_python_dependencies_backtraffic]
}

resource "aws_lambda_function" "sentry_backtraffic_proxy_lambda" {
  function_name    = "${local.lambda_backtraffic_function_name}-lambda"
  role             = aws_iam_role.sentry_backtraffic_proxy_lambda_role.arn
  handler          = "lambda_function.lambda_handler"
  memory_size      = "128"
  runtime          = local.runtime
  timeout          = "60"
  publish          = null
  filename         = data.archive_file.lambda_code.output_path
  source_code_hash = data.archive_file.lambda_code.output_base64sha256

  vpc_config {
    security_group_ids = var.deploy_lambda_in_vpc ? local.lambda_sg_ids : []
    subnet_ids         = var.deploy_lambda_in_vpc ? var.lambda_subnet_ids : []
  }

  environment {
    variables = {
      LOGGING_LEVEL     = var.env == "prod" ? "INFO" : "DEBUG"
      SENTRY_HOSTNAME   = var.sentry_hostname
      SLACK_SECRET_NAME = var.slack_secrets_arn
      JIRA_SECRET_ARN   = var.jira_secrets_arn
    }
  }

  depends_on = [aws_cloudwatch_log_group.sentry_backtraffic_proxy_lambda_log_group]
}

resource "null_resource" "clean_up_pip_files_backtraffic" {
  # If this always runs archive_file is fine, else we have an issue during refresh:
  # https://github.com/hashicorp/terraform-provider-archive/issues/78
  triggers = {
    always_run = timestamp()
  }

  provisioner "local-exec" {
    command = "bash ${path.module}/scripts/clean_dist_pkg_backtraffic.sh"

    environment = {
      source_code_dist_dir_name = local.source_code_dist_dir_name_backtraffic
      path_module               = path.module
      path_cwd                  = path.cwd
      dist_archive_file_name    = local.output_dist_file_name_backtraffic
    }
  }

  depends_on = [aws_lambda_function.sentry_backtraffic_proxy_lambda]
}

resource "aws_lambda_permission" "api_gateway_backtraffic" {
  statement_id  = "AllowAPIGatewayToInvoke"
  function_name = aws_lambda_function.sentry_backtraffic_proxy_lambda.function_name
  principal     = "apigateway.amazonaws.com"
  action        = "lambda:InvokeFunction"
  source_arn    = "${module.sentry_backtraffic_api_gateway.apigatewayv2_api_arn}/*/*"
}
