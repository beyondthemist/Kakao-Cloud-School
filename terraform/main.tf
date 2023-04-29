provider "aws" {
  region                   = var.region
  shared_credentials_files = ["$HOME/.aws/credentials"]
  profile                  = "default"
}


provider "aws" {
  alias  = "tokyo"
  region = "ap-northeast-1"
}

//data "aws_availability_zones" "available" {}

/* VPC */
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "3.19.0"

  name = "terraform-vpc"

  cidr = "10.0.0.0/16"
  //azs  = slice(data.aws_availability_zones.available.names, 0, 3)
  azs = ["ap-northeast-2a", "ap-northeast-2c"]

  private_subnets = ["10.0.1.0/24", "10.0.2.0/24"]
  public_subnets  = ["10.0.4.0/24", "10.0.5.0/24"]

  enable_nat_gateway   = true
  single_nat_gateway   = true
  enable_dns_hostnames = true

  public_subnet_tags = {
    "kubernetes.io/cluster/${var.cluster_name}" = "shared"
    "kubernetes.io/role/elb"                      = 1
  }

  private_subnet_tags = {
    "kubernetes.io/cluster/${var.cluster_name}" = "shared"
    "kubernetes.io/role/internal-elb"             = 1
  }
}
/*
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
}
*/
