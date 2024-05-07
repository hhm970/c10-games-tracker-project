resource "aws_scheduler_schedule" "c10-games-terraform-report" {
  name       = "c10-games-terraform-weekly-report"
  group_name = "default"

  flexible_time_window {
    mode = "OFF"
  }

  schedule_expression = "cron(0 9 ? * 2 *)"

  target {
    arn      = data.aws_ecs_cluster.c10-ecs-cluster.arn
    role_arn = "Need to figure out how to create ECS cluster role and permissions"

    ecs_parameters {
      task_definition_arn = aws_ecs_task_definition.weekly-report-task-def.arn
      launch_type = "FARGATE"
    }
  }
}