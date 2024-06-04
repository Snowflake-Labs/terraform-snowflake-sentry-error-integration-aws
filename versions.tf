terraform {
  required_version = ">= 1.4.6"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.38.0"
    }

    snowflake = {
      source  = "Snowflake-Labs/snowflake"
      version = ">= 0.64.0"

      configuration_aliases = [
        snowflake.api_integration_role,
        snowflake.notification_integration_role,
        snowflake.monitoring_role,
      ]
    }

    archive = {
      source  = "hashicorp/archive"
      version = "2.4.0"
    }
  }
}
