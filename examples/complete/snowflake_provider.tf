# As mentioned here from the tf snowflake provider:
# https://registry.terraform.io/providers/chanzuckerberg/snowflake/latest/docs#keypair-authentication-passhrase
# The following variables you need to set up in the environment:
# export SNOWFLAKE_USER="snowflake_username"
# export SNOWFLAKE_PRIVATE_KEY_PATH="~/.ssh/snowflake_key.p8"
# export SNOWFLAKE_PRIVATE_KEY_PASSPHRASE="snowflake_passphrase"

provider "snowflake" {
  alias = "api_integration_role"

  account = var.snowflake_account
  role    = var.integration_role
}

provider "snowflake" {
  alias = "notification_integration_role"

  account = var.snowflake_account
  role    = var.integration_role
}

provider "snowflake" {
  alias = "monitoring_role"

  account = var.snowflake_account
  role    = var.monitoring_role
}
