locals {
  source_code_repo_dir_path = "lambda-code"
  lambda_code_dir           = "lambda_src"
  output_dist_file_name     = "lambda-code.zip"
  runtime                   = "python3.9"
  source_code_dist_dir_path = "lambda-code-dist"
  upload_dir                = "sentry_integration"
  lambda_sg_ids             = var.deploy_lambda_in_vpc && length(var.lambda_security_group_ids) == 0 ? [aws_security_group.sentry_integration_lambda_sg.0.id] : var.lambda_security_group_ids
}

resource "null_resource" "install_python_dependencies" {
  # If this always runs archive_file is fine, else we have an issue during refresh:
  # https://github.com/hashicorp/terraform-provider-archive/issues/78
  triggers = {
    always_run = timestamp()
  }

  provisioner "local-exec" {
    command = "bash ${path.module}/scripts/create_dist_pkg.sh"

    environment = {
      source_code_repo_dir_path = "${local.source_code_repo_dir_path}"
      lambda_code_dir_path      = "${local.source_code_repo_dir_path}/${local.lambda_code_dir}"
      source_code_dist_dir_path = local.source_code_dist_dir_path
      source_code_upload_dir    = local.upload_dir
      runtime                   = local.runtime
      path_module               = path.module
      path_cwd                  = path.cwd
    }
  }
}

data "archive_file" "lambda_code" {
  source_dir  = "${path.module}/${local.source_code_dist_dir_path}/"
  output_path = "${path.module}/${local.output_dist_file_name}"

  type = "zip"
  excludes = [
    "__pycache__",
    ".mypy_cache",
    ".pytest_cache",
    "venv",
  ]

  depends_on = [null_resource.install_python_dependencies]
}

resource "aws_lambda_function" "sentry_integration_lambda" {
  function_name = local.lambda_function_name

  role    = aws_iam_role.sentry_integration_lambda_assume_role.arn
  handler = "sentry_integration.lambda_function.lambda_handler"

  memory_size = "4096" # 4 GB
  runtime     = local.runtime
  timeout     = "900" # 15 mins
  publish     = null

  filename         = data.archive_file.lambda_code.output_path
  source_code_hash = data.archive_file.lambda_code.output_base64sha256

  vpc_config {
    security_group_ids = var.deploy_lambda_in_vpc ? local.lambda_sg_ids : []
    subnet_ids         = var.deploy_lambda_in_vpc ? var.lambda_subnet_ids : []
  }

  depends_on = [
    aws_cloudwatch_log_group.sentry_integration_lambda_log_group
  ]
}

resource "null_resource" "clean_up_pip_files" {
  # If this always runs archive_file is fine, else we have an issue during refresh:
  # https://github.com/hashicorp/terraform-provider-archive/issues/78
  triggers = {
    always_run = timestamp()
  }

  provisioner "local-exec" {
    command = "bash ${path.module}/scripts/clean_dist_pkg.sh"

    environment = {
      source_code_dist_dir_path = local.source_code_dist_dir_path
      path_module               = path.module
      path_cwd                  = path.cwd
      dist_archive_file_name    = local.output_dist_file_name
    }
  }

  depends_on = [aws_lambda_function.sentry_integration_lambda]
}

resource "aws_lambda_permission" "api_gateway" {
  statement_id  = "AllowAPIGatewayToInvoke"
  function_name = aws_lambda_function.sentry_integration_lambda.function_name
  principal     = "apigateway.amazonaws.com"
  action        = "lambda:InvokeFunction"
  source_arn    = "${aws_api_gateway_rest_api.ef_to_lambda.execution_arn}/*/*"
}
