terraform {
  required_version = ">= 1.2.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 4.20.1"
    }

    snowflake = {
      source  = "Snowflake-Labs/snowflake"
      version = ">= 0.39.0"

      configuration_aliases = [
        snowflake.api_integration_role,
        snowflake.notification_integration_role,
      ]
    }
  }
}
