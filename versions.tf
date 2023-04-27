terraform {
  required_version = "~> 1.3.4"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.38.0"
    }

    snowflake = {
      source  = "Snowflake-Labs/snowflake"
      version = ">= 0.62.0"

      configuration_aliases = [
        snowflake.api_integration_role,
        snowflake.notification_integration_role,
        snowflake.monitoring_role,
      ]
    }
  }
}
