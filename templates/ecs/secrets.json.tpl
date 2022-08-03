[
  {
    "valueFrom": "${smtp_secrets_arn}:SMTP_DOMAIN::",
    "name": "SMTP_DOMAIN"
  },
  {
    "valueFrom": "${smtp_secrets_arn}:SMTP_USER_NAME::",
    "name": "SMTP_USER_NAME"
  },
  {
    "valueFrom": "${smtp_secrets_arn}:SMTP_PASSWORD::",
    "name": "SMTP_PASSWORD"
  },
  {
    "valueFrom": "${smtp_secrets_arn}:SMTP_SERVER::",
    "name": "SMTP_SERVER"
  },
  {
    "valueFrom": "${db_secrets_arn}:DATABASE_USERNAME::",
    "name": "DATABASE_USERNAME"
  },
  {
    "valueFrom": "${db_secrets_arn}:DATABASE_PASSWORD::",
    "name": "DATABASE_PASSWORD"
  },
  {
    "valueFrom": "${db_secrets_arn}:DATABASE_NAME::",
    "name": "DATABASE_NAME"
  },
  {
    "valueFrom": "${tines_secrets_arn}:APP_SECRET_TOKEN::",
    "name": "APP_SECRET_TOKEN"
  },

  {
    "valueFrom": "${tines_secrets_arn}:TEMPLATE_TENANT_INDEX::",
    "name": "TEMPLATE_TENANT_INDEX"
  },
  {
    "valueFrom": "${tines_secrets_arn}:TEMPLATE_TENANT_WRITE_KEY::",
    "name": "TEMPLATE_TENANT_WRITE_KEY"
  }
]
