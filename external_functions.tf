resource "snowflake_external_function" "send_to_sentry" {
  provider = snowflake.monitoring_role

  database = "SNOWALERT"
  schema   = "MONITORING"
  name     = "SEND_TO_SENTRY"

  # Function arguments
  arg {
    name = "DSN"
    type = "VARCHAR(16777216)"
  }

  arg {
    name = "NAME"
    type = "VARCHAR(16777216)"
  }

  arg {
    name = "HISTORY_TYPE"
    type = "VARCHAR(16777216)"
  }

  arg {
    name = "ERROR"
    type = "VARCHAR(16777216)"
  }

  arg {
    name = "TS"
    type = "VARCHAR(16777216)"
  }

  arg {
    name = "HISTORY_URL"
    type = "VARCHAR(16777216)"
  }

  # Function headers
  header {
    name  = "dsn"
    value = "{0}"
  }

  header {
    name  = "name"
    value = "{1}"
  }

  header {
    name  = "history-type"
    value = "{2}"
  }

  header {
    name  = "error"
    value = "{3}"
  }

  header {
    name  = "ts"
    value = "{4}"
  }

  header {
    name  = "history-url"
    value = "{5}"
  }

  return_null_allowed       = true
  api_integration           = snowflake_api_integration.sentry_integration_api_integration.name
  url_of_proxy_and_resource = "${aws_api_gateway_deployment.sentry_integration_api_gw_deployment.invoke_url}${var.env}/sentry_logger"

  return_type     = "VARIANT"
  return_behavior = "VOLATILE"

  comment = <<COMMENT
SEND_TO_SENTRY: (dsn, name, history_type, error, ts, history_url) -> response
COMMENT
}
