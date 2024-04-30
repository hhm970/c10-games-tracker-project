output "dashboard_base_url" {
value = aws_ecs_service.games-dashboard.address
description = "A URL link to our games tracker dashboard."
}