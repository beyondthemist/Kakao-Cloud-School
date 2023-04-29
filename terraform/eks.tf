module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "19.10.0"

  cluster_name    = var.cluster_name
  cluster_version = "1.24"


  vpc_id                         = module.vpc.vpc_id
  subnet_ids                     = module.vpc.private_subnets
  cluster_endpoint_public_access = true

  eks_managed_node_group_defaults = {
    ami_type = "AL2_x86_64"
  }

  eks_managed_node_groups = {
    node_group_in_az_a = {
      name = "node-group-1"

      instance_types = ["t2.medium"]

      min_size     = 1
      max_size     = 3
      desired_size = 2
      subnets = [module.vpc.private_subnets[0]]
    }

    node_group_in_az_c = {
      name = "node-group-2"

      instance_types = ["t2.medium"]

      min_size     = 1
      max_size     = 3
      desired_size = 2
      subnets = [module.vpc.private_subnets[1]]
    }
  }

  cluster_additional_security_group_ids = [
    aws_security_group.eks_worker_sg.id
  ] 
}
