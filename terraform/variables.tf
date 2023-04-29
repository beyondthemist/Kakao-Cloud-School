variable "region" {
  description = "AWS region"
  type        = string
  default     = "ap-northeast-2" //Seoul
}

variable "cluster_name" {
  description = "EKS cluster name"
  type        = string
  default     = "terraform-eks"
}

variable "db_instance_name" {
  description = "DB instance name"
  type        = string
  default     = "project"
}

variable "db_name" {
  description = "DB name"
  type        = string
  default     = "content"
}

variable "db_instance_class" {
  description = "DB instance class"
  type        = string
  default     = "db.t3.micro"
}

variable "db_allocated_storage" {
  description = "Gibibytes to be allocated to DB instance"
  type        = string
  default     = "10"
}

variable "db_engine" {
  description = "Engine to be used to DB instance"
  type        = string
  default     = "mariadb"
}

variable "db_engine_version" {
  description = "Engine to be used to DB instance"
  type        = string
  default     = "10.6.10"
}

variable "db_username" {
  description = "User name to connect to DB instance"
  type        = string
  sensitive   = true
  default     = "root"
}

variable "db_password" {
  description = "RDS root user password"
  type        = string
  sensitive   = true
  default     = "password"
}
