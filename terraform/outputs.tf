output "cluster_endpoint" {
  description = "Endpoint for EKS control plane"
  value       = module.eks.cluster_endpoint
}

/*
output "vpc_id" {
  value = module.vpc.vpc_id
}

output "public_subnet_id" {
  desciption = 
  value = module.vpc.public_subnets.this[0]
}
*/
output "cluster_security_group_id" {
  description = "Security group ids attached to the cluster control plane"
  value       = module.eks.cluster_security_group_id
}

output "region" {
  description = "AWS region"
  value       = var.region
}

output "cluster_name" {
  description = "Kubernetes Cluster Name"
  value       = module.eks.cluster_name
}

output "bastion_sg_id" {
  description = "bastion_sg"
  value = aws_security_group.bastion_sg.id
}

/*
output "s3_bucket_id" {
    description = "S3 Bucket"
    value = module.s3_bucket.s3_bucket_id
}
*/

output "s3_bucket_id" {
  description = "source bucket"
  value = resource.aws_s3_bucket_versioning.source
}

output "eks_cluster_security_group_id" {
  value = module.eks.cluster_security_group_id
}
