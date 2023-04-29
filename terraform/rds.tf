resource "aws_db_subnet_group" "rds_subnet_group" {
  name = "rds_subnet_group"
  subnet_ids = module.vpc.private_subnets

  tags = {
    Name = "RDS subnet group"
  }
}

resource "aws_db_parameter_group" "default" {
  name   = "mariadb-pg"
  family = "mariadb10.6"

  parameter {
    name  = "character_set_client"
    value = "utf8mb4"
  }

  parameter {
    name  = "character_set_connection"
    value = "utf8mb4"
  }

  parameter {
    name  = "character_set_database"
    value = "utf8mb4"
  }

  parameter {
    name  = "character_set_filesystem"
    value = "utf8mb4"
  }

  parameter {
    name  = "character_set_results"
    value = "utf8mb4"
  }

  parameter {
    name  = "character_set_server"
    value = "utf8mb4"
  }
}

resource "aws_db_instance" "source" {
  identifier             = "source"
  instance_class         = var.db_instance_class
  allocated_storage      = var.db_allocated_storage
  db_name                = var.db_name
  engine                 = var.db_engine
  engine_version         = var.db_engine_version
  username               = var.db_username
  password               = var.db_password
  db_subnet_group_name   = aws_db_subnet_group.rds_subnet_group.name
  vpc_security_group_ids = [aws_security_group.rds_sg.id]
  parameter_group_name   = aws_db_parameter_group.default.name
  publicly_accessible    = true //false
  skip_final_snapshot    = true // Take final snapshot when destroying resources if false
  // final_snapshot_identifier = "final-snapshot-of-source-rds" // required if skip_final_snapshot is true
  multi_az = true	  
  backup_retention_period = 3
  provider               = aws
}

/*
resource "aws_db_instance" "destination" {
  replicate_source_db     = aws_db_instance.source.arn
  instance_class          = var.db_instance_class
  publicly_accessible     = false
  skip_final_snapshot     = true
  replica_mode            = "open-read-only"
  backup_retention_period = 3
  availability_zone       = "ap-northeast-2c"
}


resource "aws_kms_key" "destination" {
  description = "Encryption key for automated backups"

  provider = aws.tokyo
}
*/

resource "aws_db_instance_automated_backups_replication" "default" {
  source_db_instance_arn = aws_db_instance.source.arn
  // kms_key_id             = aws_kms_key.destination.arn

  provider               = aws.tokyo
}
