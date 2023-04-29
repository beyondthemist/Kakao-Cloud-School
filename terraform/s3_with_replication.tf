/* Required IAM policies and roles for cross-region replication of S3 bucket */
resource "aws_iam_role" "replication" {
  name               = "tf-iam-role-replication-test"
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
}

data "aws_iam_policy_document" "assume_role" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["s3.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}


data "aws_iam_policy_document" "replication" {
  statement {
    effect = "Allow"

    actions = [
      "s3:GetReplicationConfiguration",
      "s3:ListBucket",
          "s3:DeleteMarkerReplication"
    ]

    resources = [aws_s3_bucket.source.arn]
  }

  statement {
    effect = "Allow"

    actions = [
      "s3:GetObjectVersionForReplication",
      "s3:GetObjectVersionAcl",
      "s3:GetObjectVersionTagging",
    ]

    resources = ["${aws_s3_bucket.source.arn}/*"]
  }

  statement {
    effect = "Allow"

    actions = [
      "s3:ReplicateObject",
      "s3:ReplicateDelete",
      "s3:ReplicateTags",
    ]

    resources = ["${aws_s3_bucket.destination.arn}/*"]
  }
}

resource "aws_iam_policy" "replication" {
  name   = "tf-iam-role-policy-replication-test"
  policy = data.aws_iam_policy_document.replication.json
}

resource "aws_iam_role_policy_attachment" "replication" {
  role       = aws_iam_role.replication.name
  policy_arn = aws_iam_policy.replication.arn
}


/* Destination S3 bucket */
resource "aws_s3_bucket" "destination" {
  provider = aws.tokyo
  bucket = "destination-tokyo-s3-bucket"
  versioning {
    enabled = true
  }
}

resource "aws_s3_bucket_versioning" "destination" {
  provider = aws.tokyo
  bucket = aws_s3_bucket.destination.id
  versioning_configuration {
    status = "Enabled"
  }
}


/* Source S3 bucket */
resource "aws_s3_bucket" "source" {
  provider = aws
  bucket   = "source-seoul-s3-bucket"
  versioning {
    enabled = true
  }
}

/*
resource "aws_s3_bucket_acl" "source_bucket_acl" {
  provider = aws

  bucket = aws_s3_bucket.source.id
  acl    = "private"
}
*/
resource "aws_s3_bucket_versioning" "source" {
  provider = aws

  bucket = aws_s3_bucket.source.id
  versioning_configuration {
    status = "Enabled"
  }
}


/* S3 bucket replication */
resource "aws_s3_bucket_replication_configuration" "replication" {
  provider = aws

  # Must have bucket versioning enabled first
  depends_on = [aws_s3_bucket_versioning.source]

  role   = aws_iam_role.replication.arn
  bucket = aws_s3_bucket_versioning.source.id

  rule {
    status = "Enabled"

    destination {
      bucket        = "${aws_s3_bucket.destination.arn}"
      storage_class = "STANDARD"
    }
    /*
    delete_marker_replication {
      status = "Disabled"
    }
    */
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "example" {
  bucket = aws_s3_bucket_versioning.source.bucket
  rule {
    id      = "velero-backup-rule"
    status  = "Enabled"
    prefix  = "backups/"

    expiration {
      days = 30
    }
  }
}
