data "aws_iam_policy_document" "eventbridge-report-permissions-policy" {
  statement {
    effect = "Allow"

    resources = ["*"]
 
    actions = ["states:StartExecution"]
  }
}

data "aws_iam_policy_document" "eventbridge-report-trust-policy" {
  statement {
    effect = "Allow"

    principals {
       type        = "Service"
       identifiers = ["scheduler.amazonaws.com"]
     }
 
    actions = ["sts:AssumeRole"]
  }
}


resource "aws_iam_role" "ecs-task-role" {
  name               = "c10-games-terraform-eventbridge-role-report-tf"
  assume_role_policy = data.aws_iam_policy_document.eventbridge-trust-policy.json
  inline_policy {
    name = "ecsTaskExecutionRole"
    policy = data.aws_iam_policy_document.eventbridge-permissions-policy.json
  }
}


data "aws_ecr_repository" "ecr-repo-weekly-report" {
  name = "c10-games-weekly-report"
}

data "aws_ecr_image" "ecr-image-weekly-report" {
  repository_name = data.aws_ecr_repository.ecr-repo-weekly-report.name
  image_tag       = "latest"
}

resource "aws_ecs_task_definition" "weekly-report-task-def" {
  family                = "c10-games-weekly-report-task-def"
  container_definitions = jsonencode([
    {
      name         = "games-weekly-report"
      image        = "129033205317.dkr.ecr.eu-west-2.amazonaws.com/c10-games-weekly-report"
      essential    = true
      "environment": [
                {
                    "name": "AWS_KEY",
                    "value": var.AWS_KEY
                },
                {
                    "name": "AWS_SECRET",
                    "value": var.AWS_SECRET
                },
                {
                    "name": "DB_PORT",
                    "value": var.DB_PORT
                },
                {
                    "name": "DB_USER",
                    "value": var.DB_USER
                },
                {
                    "name": "DB_NAME",
                    "value": var.DB_NAME
                },
                {
                    "name": "DB_HOST",
                    "value": var.DB_HOST
                },
                {
                    "name": "DB_PASSWORD",
                    "value": var.DB_PASSWORD
                },
                {
                  "name": "STORAGE_FOLDER",
                  "value": "diagrams"
                }
      ]
    }
  ])
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  memory                   = 3072
  cpu                      = 1024
  execution_role_arn       = resource.aws_iam_role.ecs-task-role.arn
}