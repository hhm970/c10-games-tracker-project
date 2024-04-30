data "aws_iam_role" "ecs-role" {
    name = "ecsTaskExecutionRole"
}

resource "aws_ecs_task_definition" "dashboard-task-definition" {
  family                = "c10-games-dashboard-task-tf"
  container_definitions = jsonencode([
    {
      name         = "games-dashboard-tf"
      image        = "129033205317.dkr.ecr.eu-west-2.amazonaws.com/c10-games-dashboard:latest"
      essential    = true
      portMappings = [
        {
          containerPort = 8501,
          hostPort = 8501
        }
      ],
      "environment": [
                {
                    "name": "AWS_KEY",
                    "value": var.AWS_KEY
                },
                {
                    "name": "AWS_SECRET",
                    "value": var.AWS_SECRET
                },
                {
                    "name": "DB_PORT",
                    "value": var.DB_PORT
                },
                {
                    "name": "DB_USER",
                    "value": var.DB_USER
                },
                {
                    "name": "DB_NAME",
                    "value": var.DB_NAME
                },
                {
                    "name": "DB_HOST",
                    "value": var.DB_HOST
                },
                {
                    "name": "DB_PASSWORD",
                    "value": var.DB_PASSWORD
                }
      ]
    }
  ])
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  memory                   = 3072
  cpu                      = 1024
  execution_role_arn       = data.aws_iam_role.ecs-role.arn
}

data "aws_vpc" "cohort-10-vpc" {
  id = var.VPC_ID
}

data "aws_ecs_cluster" "c10-ecs-cluster" {
  cluster_name = "c10-ecs-cluster"
}

data "aws_subnet" "subnet-1" {
  filter {
    name   = "tag:Name"
    values = ["cohort-10-public-subnet-1"]
  }
}

data "aws_subnet" "subnet-2" {
  filter {
    name   = "tag:Name"
    values = ["cohort-10-public-subnet-2"]
  }
}

data "aws_subnet" "subnet-3" {
  filter {
    name   = "tag:Name"
    values = ["cohort-10-public-subnet-3"]
  }
}

resource "aws_ecs_service" "games-dashboard" {
  name            = "c10-games-dashboard-tf"
  cluster         = data.aws_ecs_cluster.c10-ecs-cluster.id
  task_definition = aws_ecs_task_definition.dashboard-task-definition.arn
  launch_type     = "FARGATE"
  desired_count   = 1

  network_configuration {
    subnets          = [data.aws_subnet.subnet-1.id, data.aws_subnet.subnet-2.id, data.aws_subnet.subnet-3.id]
    security_groups  = [aws_security_group.dashboard_security_group.id]
    assign_public_ip = true
  }

  deployment_controller {
    type = "ECS"
  }
}

resource "aws_security_group" "dashboard_security_group" {
    name = "c10-games-dashboard-sg-tf"
    vpc_id = data.aws_vpc.cohort-10-vpc.id
}

resource "aws_security_group_rule" "allow-all-ipv4-traffic-dashboard" {
  type              = "ingress"
  from_port         = 8501
  to_port           = 8501
  protocol          = "tcp"
  cidr_blocks       = ["0.0.0.0/0"]
  security_group_id = aws_security_group.dashboard_security_group.id
}

resource "aws_security_group_rule" "allow-all-ipv6-traffic-dashboard" {
  type              = "ingress"
  from_port         = 8501
  to_port           = 8501
  protocol          = "tcp"
  ipv6_cidr_blocks  = ["::/0"]
  security_group_id = aws_security_group.dashboard_security_group.id
}

resource "aws_security_group_rule" "allow_tcp_traffic" {
  type              = "ingress"
  from_port         = 80
  to_port           = 80
  protocol          = "tcp"
  cidr_blocks  = ["0.0.0.0/0"]
  security_group_id = aws_security_group.dashboard_security_group.id
}

resource "aws_security_group_rule" "allow_all_outbound_traffic" {
  type              = "egress"
  from_port         = 0
  to_port           = 0
  protocol          = "-1"
  cidr_blocks  = ["0.0.0.0/0"]
  security_group_id = aws_security_group.dashboard_security_group.id
}