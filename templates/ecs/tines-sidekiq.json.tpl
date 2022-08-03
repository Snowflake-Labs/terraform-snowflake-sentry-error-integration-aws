[
  {
    "name": "tines-sidekiq",
    "command": [
      "start-tines-sidekiq"
    ],
    "image": "${tines_app_image_version}",
    "environment": ${envs},
    "secrets": ${secrets},
    "logConfiguration": {
      "logDriver": "awslogs",
      "options": {
        "awslogs-group": "/aws/ecs-${env}/tines-sidekiq",
        "awslogs-region": "${aws_region}",
        "awslogs-stream-prefix": "tines"
      }
    }
  },
  {
    "name": "sql-over-http",
    "image": "${tines_soh_image_version}",
    "environment": [
      {
        "name": "PORT",
        "value": "4000"
      }
    ],
    "logConfiguration": {
      "logDriver": "awslogs",
      "options": {
        "awslogs-group": "/aws/ecs-${env}/tines-sidekiq",
        "awslogs-region": "${aws_region}",
        "awslogs-stream-prefix": "tines"
      }
    },
    "portMappings": [
      {
        "containerPort": 4000,
        "hostPort": 4000,
        "protocol": "tcp"
      }
    ]
  }
] 
