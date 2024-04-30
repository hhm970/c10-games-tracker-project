data "aws_iam_policy_document" "eventbridge-permissions-policy" {
  statement {
    effect = "Allow"

    resources = ["*"]
 
    actions = ["states:StartExecution"]
  }
}

data "aws_iam_policy_document" "eventbridge-trust-policy" {
  statement {
    effect = "Allow"

    principals {
       type        = "Service"
       identifiers = ["scheduler.amazonaws.com"]
     }
 
    actions = ["sts:AssumeRole"]
  }
}


resource "aws_iam_role" "eventbridge-role" {
  name               = "c10-games-terraform-eventbrige-role-pipeline"
  assume_role_policy = data.aws_iam_policy_document.eventbridge-trust-policy.json
  inline_policy {
    name = "c10-games-inline-step-function"
    policy = data.aws_iam_policy_document.eventbridge-permissions-policy.json
  }
}


resource "aws_scheduler_schedule" "c10-games-terraform-pipeline" {
  name       = "c10-games-terraform-pipeline"
  group_name = "default"

  flexible_time_window {
    mode = "OFF"
  }

  schedule_expression = "cron(50 23 * * ? *)"

  target {
    arn      = "arn:aws:states:eu-west-2:129033205317:stateMachine:c10-games-statemachine-terraform"
    role_arn = aws_iam_role.eventbridge-role.arn
  }
}