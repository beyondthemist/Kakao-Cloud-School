resource "aws_security_group" "eks_worker_sg" {
  name_prefix = "eks-worker-sg-"
  vpc_id      = module.vpc.vpc_id

  # Add any necessary inbound or outbound rules here
  ingress {
    from_port = 9090
    to_port   = 9090
    protocol  = "tcp"
    cidr_blocks = module.vpc.private_subnets_cidr_blocks
  }

  ingress {
    from_port = 9100
    to_port   = 9100
    protocol  = "tcp"
    cidr_blocks = module.vpc.private_subnets_cidr_blocks
  }
}
