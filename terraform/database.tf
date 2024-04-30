resource "aws_db_instance" "rds_instance" {
  allocated_storage    = 20
  db_name              = var.DB_NAME
  engine               = "postgres"
  engine_version       = "16.1"
  instance_class       = "db.t3.micro"
  publicly_accessible          = true
  performance_insights_enabled = false
  skip_final_snapshot  = true
  db_subnet_group_name         = data.aws_db_subnet_group.public_subnet_group.name
  vpc_security_group_ids       = [aws_security_group.rds_security_group.id]
  username             = var.DB_USER
  password             = var.DB_PASSWORD
}

resource "aws_security_group" "rds_security_group" {
    name = "c10-games-tracker-sg-tf"
    vpc_id = "vpc-0c4f01396d92e1cc7"
}

resource "aws_security_group_rule" "allow-all-ipv4-traffic" {
  type              = "ingress"
  from_port         = 5432
  to_port           = 5432
  protocol          = "tcp"
  cidr_blocks       = ["0.0.0.0/0"]
  security_group_id = aws_security_group.rds_security_group.id
}

data "aws_db_subnet_group" "public_subnet_group" {
    name = "public_subnet_group"
}
