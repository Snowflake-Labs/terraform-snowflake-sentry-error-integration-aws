resource "snowflake_function_grant" "send_to_sentry_function_grant_usage" {
  provider = snowflake.monitoring_role

  database_name = var.database
  schema_name   = var.monitoring_schema
  function_name = snowflake_external_function.send_to_sentry.name
  argument_data_types = [
    "VARCHAR",
    "VARCHAR",
    "VARCHAR",
    "VARCHAR",
    "VARCHAR",
    "VARCHAR",
  ]
  privilege              = "USAGE"
  roles                  = var.send_to_sentry_function_user_roles
  enable_multiple_grants = true

  depends_on = [
    snowflake_external_function.send_to_sentry
  ]
}
