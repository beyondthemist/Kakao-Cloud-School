resource "aws_security_group" "bastion_sg" {
  name = "bastion_sg"
  description = "inbound all"
  vpc_id = module.vpc.vpc_id

  ingress {
    description = "HTTPS"
    from_port = 443
    to_port = 443
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "HTTPS"
    from_port = 80
    to_port = 80
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "SSH"
    from_port = 22
    to_port = 22
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }


  egress = [
    {
      description = "outbound all"
        from_port = 0
        to_port = 0
        protocol = "-1"
        cidr_blocks = ["0.0.0.0/0"]
        ipv6_cidr_blocks = []
        aws_security_groups = []
        prefix_list_ids = []
        self = false
        security_groups = []
     }
   ]
   tags = {
     Name = "Inbound & outbound allow all"
   }
}

resource "aws_security_group_rule" "allow_ingress" {
  type        = "ingress"
  from_port   = 0
  to_port     = 0
  protocol    = "-1"
  cidr_blocks = ["0.0.0.0/0"]
  security_group_id = module.eks.cluster_security_group_id
}


