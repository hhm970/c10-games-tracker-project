output "dashboard_base_url" {
    value = aws_ecs_service.games-dashboard.address
    description = "A URL link to our games tracker dashboard."
}

output "rds_instance_address" {
  value       = aws_db_instance.rds_instance.address
  description = "The public IP address of the RDS instance."
}