resource "aws_scheduler_schedule" "c10-games-terraform-report" {
  name       = "c10-games-terraform-report"
  group_name = "default"

  flexible_time_window {
    mode = "OFF"
  }

  schedule_expression = "cron(0 9 ? * 2 *)"

  target {
    arn      = "arn:aws:states:eu-west-2:129033205317:stateMachine:c10-games-statemachine-terraform-report"
    role_arn = aws_iam_role.eventbridge-role.arn
  }
}