resource "aws_db_instance" "default" {
  allocated_storage    = 20
  db_name              = "games"
  engine               = "postgres"
  engine_version       = "16.1"
  instance_class       = "db.t3.micro"
  publicly_accessible          = true
  performance_insights_enabled = false
  username             = var.DB_USER
  password             = var.DB_PASSWORD
  skip_final_snapshot  = true
  db_subnet_group_name         = data.aws_db_subnet_group.public_subnet_group.name
  vpc_security_group_ids       = [aws_security_group.rds_security_group.id]
}

