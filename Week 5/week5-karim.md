+++
title = "Shahid's Blog. Week 5"
date = "2018-09-28"
+++

## Shahid's Blog. Week 5
#### What's new this week?

##### Setting up a S3 bucket on the AWS console
1. Visit the AWS console at https://aws.amazon.com/console/
2. Under the AWS services title, in the search bar type ```s3```.
3. Under the Amazon S3 title, click the Create bucket button.
4. A window will pop up where you will need to name the bucket. Name it something descriptive to your uses.
5. Versioning should be checked since this option forces the bucket to track changes to an object. As long as this option is on, new objects uploaded to the bucket will have an id number. Each time the object is updated, the id number will change.
6. Server access logging should also be enabled in order to track requests to the bucket. Point the storage of these logs to the s3 bucket you are creating.
7. For added security, enable the default encryption with the AES-256 option. This will encrypt all your data with an amazon supplied AES-256 key.
8. Since we opted for the extra security we will want to leave the manage public permissions to do not grant public read access.    
9. Finally press the button to create the bucket.

##### Configuring lifecycle for the newly created S3 bucket on the AWS console
1. Once you've finished creating a new bucket, you'll be returned to the Amazon s3 console page. From there, press on the link to the new s3 bucket.
2. Click on the Management tab.
3. Click on the add lifecycle rule.
4. A window will open asking for a rule name. Provide a descriptive one.
5. Configure transitions for current and previous versions of your objects. Choose the best option for you out of these three:
  ```
  a) Transition to Standard-IA after x amount of days (Minimum 30 days)
  b) Transition to One Zone-IA after x amount of days (Minimum 30 days)
  c) Transition to Amazon Glacier after x amount of days (No minimum)
  ```
6. Configure your current and previous versions of objects to expire after a fixed amount of time (Minimum 31 days)

    6a. Configure incomplete multipart uploads to expire after a certain amount of days.

The benefit of choice a) is that the objects are stored in at least 3 geographically separated regions. The price is marginally higher than the other options.

The benefit of choice b) is that the price is marginally lower than the other options. As a tradeoff for this price decrease, the objects are only stored in one location. This makes the objects susceptible to loss through earthquake, flood, or other natural disaster.

The benefit of choice c) is the heavily reduced price per GB. The drawback being the time it takes to retrieve the stored objects and the cost associated with retrieval.

##### Setting up a S3 bucket with terraform
```
resource "aws_s3_bucket" "bucket" {
  bucket = "my-bucket"
  acl    = "private"

  # How long the current version should stay in the bucket
  # before being moved to the transition zones
  lifecycle_rule {
    id      = "log"
    enabled = true

    prefix  = "log/"
    tags {
      "rule"      = "log"
      "autoclean" = "true"
    }

    transition {
      days = 15
      storage_class = "ONEZONE_IA"
    }

    transition {
      days          = 30
      storage_class = "STANDARD_IA"
    }

    transition {
      days          = 60
      storage_class = "GLACIER"
    }

    expiration {
      days = 90
    }
  }

  lifecycle_rule {
    id      = "tmp"
    prefix  = "tmp/"
    enabled = true

    expiration {
      date = "2018-10-10"
    }
  }
}

resource "aws_s3_bucket" "versioning_bucket" {
  bucket = "my-versioning-bucket"
  acl    = "private"

  versioning {
    enabled = true
  }

  lifecycle_rule {
    prefix  = "config/"
    enabled = true

    noncurrent_version_transition {
      days          = 30
      storage_class = "STANDARD_IA"
    }

    noncurrent_version_transition {
      days          = 60
      storage_class = "GLACIER"
    }

    noncurrent_version_expiration {
      days = 90
    }
  }

    resource "aws_kms_key" "mykey" {
    description             = "This key is used to encrypt bucket objects"
    deletion_window_in_days = 10
  }

  # Using server side encryption for all objects in the bucket
  resource "aws_s3_bucket" "mybucket" {
    bucket = "mybucket"
    server_side_encryption_configuration {
      rule {
        apply_server_side_encryption_by_default {
          kms_master_key_id = "${aws_kms_key.mykey.arn}"
          sse_algorithm     = "aws:kms"
        }
      }
    }
  }
}
```
