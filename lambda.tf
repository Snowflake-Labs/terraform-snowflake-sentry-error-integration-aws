locals {
  source_code_path          = "lambda-code"
  output_dist_file_name     = "lambda-code.zip"
  runtime                   = "python3.8"
  source_code_dist_dir_name = "lambda-code-dist"
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
      source_code_path          = local.source_code_path
      source_code_dist_dir_name = local.source_code_dist_dir_name
      runtime                   = local.runtime
      path_module               = path.module
      path_cwd                  = path.cwd
    }
  }
}

data "archive_file" "lambda_code" {
  source_dir  = "${path.module}/${local.source_code_dist_dir_name}/"
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

resource "aws_lambda_function" "tines_lambda" {
  function_name    = local.lambda_function_name
  role             = aws_iam_role.tines_lambda_role.arn
  handler          = "lambda_function.lambda_handler"
  memory_size      = "128"
  runtime          = local.runtime
  timeout          = "60"
  publish          = null
  filename         = data.archive_file.lambda_code.output_path
  source_code_hash = data.archive_file.lambda_code.output_base64sha256

  vpc_config {
    subnet_ids         = var.private_subnets
    security_group_ids = [aws_security_group.tines_lambda.id]
  }

  depends_on = [aws_cloudwatch_log_group.tines_lambda_log_group]
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
      source_code_dist_dir_name = local.source_code_dist_dir_name
      path_module               = path.module
      path_cwd                  = path.cwd
      dist_archive_file_name    = local.output_dist_file_name
    }
  }

  depends_on = [aws_lambda_function.tines_lambda]
}

resource "aws_lambda_permission" "api_gateway" {
  statement_id  = "AllowAPIGatewayToInvoke"
  function_name = aws_lambda_function.tines_lambda.function_name
  principal     = "apigateway.amazonaws.com"
  action        = "lambda:InvokeFunction"
  source_arn    = "${module.api_gateway.apigatewayv2_api_arn}/*/*"
}
