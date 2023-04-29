resource "aws_security_group" "rds_sg" {
  name        = "allow_rds"
  description = "Only TCP 3306 traffic is allowed for inbound"
  vpc_id      = module.vpc.vpc_id


  ingress {
    from_port   = 3306
    to_port     = 3306
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

