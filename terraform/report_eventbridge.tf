resource "aws_scheduler_schedule" "c10-games-terraform-report" {
  name       = "c10-games-terraform-weekly-report"
  group_name = "default"

  flexible_time_window {
    mode = "OFF"
  }

  schedule_expression = "cron(0 9 ? * 2 *)"

  target {
    arn      = data.aws_ecs_cluster.c10-ecs-cluster.arn
    role_arn = aws_iam_role.ecs-task-role.arn

    ecs_parameters {
      task_definition_arn = aws_ecs_task_definition.weekly-report-task-def.arn
      launch_type = "FARGATE"
      task_count = 1
      enable_ecs_managed_tags = true
      enable_execute_command = false
      network_configuration {
        subnets = [
          "subnet-0f1bc89d0670672b5",
          "subnet-010c8f9ace38ac103",
          "subnet-05a01546985e339a6"
          ]
      }
    }
  }
}