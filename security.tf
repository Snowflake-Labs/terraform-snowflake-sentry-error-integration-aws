resource "aws_security_group" "sentry_integration_lambda_sg" {
  count = var.deploy_lambda_in_vpc && length(var.lambda_security_group_ids) == 0 ? 1 : 0

  name        = "${local.sentry_integration_prefix}-lambda-sg"
  description = "Create security group for lambda if not provided."
  vpc_id      = var.vpc_id
}

resource "aws_security_group_rule" "sentry_integration_lambda_sg_egress_rule" {
  count = var.deploy_lambda_in_vpc && length(var.lambda_security_group_ids) == 0 ? 1 : 0

  type        = "egress"
  to_port     = 0
  from_port   = 0
  protocol    = "-1"
  cidr_blocks = ["0.0.0.0/0"]

  security_group_id = aws_security_group.sentry_integration_lambda_sg.0.id
}
