resource "aws_scheduler_schedule" "c10-games-terraform-report" {
  name       = "c10-games-terraform-report-tf"
  group_name = "default"

  flexible_time_window {
    mode = "OFF"
  }

  schedule_expression = "cron(0 9 ? * 2 *)"

  target {
    arn      = aws_ecs_task_definition.weekly-report-task-def.arn
    role_arn = data.aws_iam_role.ecs-role.arn
  }
}