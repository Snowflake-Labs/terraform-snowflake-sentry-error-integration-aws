[
  {
    "name": "tines-seeder",
    "image": "${tines_app_image_version}",
    "environment": ${envs_seeder},
    "essential": false,
    "secrets": ${secrets},
    "command": ["prepare-database"],
    "logConfiguration": {
      "logDriver": "awslogs",
      "options": {
        "awslogs-group": "/aws/ecs-${env}/tines-seeder",
        "awslogs-region": "${aws_region}",
        "awslogs-stream-prefix": "tines"
      }
    }
  },
  {
    "command": [
      "start-tines-app"
    ],
    "name": "tines-app",
    "image": "${tines_app_image_version}",
    "environment": ${envs},
    "secrets": ${secrets},
    "dependsOn": [
      {
        "containerName": "tines-seeder",
        "condition": "SUCCESS"
      }
    ],
    "essential": true,
    "logConfiguration": {
      "logDriver": "awslogs",
      "options": {
        "awslogs-group": "/aws/ecs-${env}/tines-app",
        "awslogs-region": "${aws_region}",
        "awslogs-stream-prefix": "tines"
      }
    },
    "portMappings": [
      {"containerPort": 3000}
    ]
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
        "awslogs-group": "/aws/ecs-${env}/tines-app",
        "awslogs-region": "${aws_region}",
        "awslogs-stream-prefix": "tines"
      }
    },
    "portMappings": [
      {"containerPort": 4000}
    ]
  }
]
