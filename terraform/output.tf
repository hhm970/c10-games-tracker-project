output "rds_instance_address" {
  value       = aws_db_instance.rds_instance.address
  description = "The public IP address of the RDS instance."
}