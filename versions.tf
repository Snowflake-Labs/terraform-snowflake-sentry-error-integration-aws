terraform {
  required_version = ">= 1.2.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 4.20.1"
    }

    snowflake = {
      source  = "Snowflake-Labs/snowflake"
      version = ">= 0.40.0"

      configuration_aliases = [
        snowflake.security_api_integration_role,
        snowflake.security_notification_integration_role,
        snowflake.security_monitoring_role,
      ]
    }
  }
}
