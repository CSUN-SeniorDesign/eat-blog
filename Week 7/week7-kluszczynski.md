## Tyler's Blog. Week 7.
#### What's new this week?

##### Starting Project 3
This week has been the best week so far this semester in my view. We are attempting a new project management strategy where everyone is given tasks that they are responsible for, that can be done without prerequisites being completed. For example, I am doing Lambda while Alex and Shahid are doing docker, Erik and Brian are working on AWS.

##### Lambda Overview
I haven't used Lambda before, so this was my first introduction. It seems simple enough, AWS will run your code on a server, then cleanup everything you do after it's done running, but it is actually quite complicated to get everything set up correctly. In fact, lambda requires Terraform setup for VPC access, IAM roles and policies (for the bucket the file is stored in, and for lambda itself), and logging permissions. On top of that, you actually have to write the python code.

##### Terraform modification for Lambda
This blog, I'm going to cover the Terraform modification  required for lambda to actually run (so far), as it seems this is an overlooked part of the process (it doesn't even appear on the project breakdown sheet).

###### Updating S3 Bucket
Here's the Terraform code to get the bucket working:

```
resource "aws_s3_bucket_notification" "bucket_notification" {
  bucket = "${aws_s3_bucket.bucket.id}"

  lambda_function {
    lambda_function_arn = "${aws_lambda_function.test-lambda.arn}"
    events              = ["s3:ObjectCreated:*"]
    filter_suffix       = ".txt"
  }
}
```

```
resource "aws_lambda_permission" "allow_bucket" {
  statement_id  = "AllowExecutionFromS3Bucket"
  action        = "lambda:InvokeFunction"
  function_name = "${aws_lambda_function.test-lambda.arn}"
  principal     = "s3.amazonaws.com"
  source_arn    = "${aws_s3_bucket.bucket.arn}"
}

```
Note that the bucket must be given permissions, and the lambda function must also be given permissions to access the bucket. I also had to create a new role and policy for Lambda as well.

###### Lambda Role and Policy
Here is the lambda policy. Note that in the "abridged" sections, there is a list of different actions and resources that Lambda is allowed to update and use:
```
resource "aws_iam_policy" "LP" {
  name = "LP_Policy"
  path = "/"
  description = "Policy for lambda."
  policy =<<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                <abridged>
            "Resource": [
                <abridged>
            ]
        },
        {
            "Sid": "VisualEditor1",
            "Effect": "Allow",
            "Action": [
                <abridged>
            ],
            "Resource": "*"
        },
        {
            "Sid": "VisualEditor2",
            "Effect": "Allow",
            "Action": [
                <abridged>
            ],
            "Resource": [
                "arn:aws:logs:*:*:log-group:*:*:*",
                "arn:aws:s3:::*/*"
            ]
        }
    ]
}
EOF
}
```
Here is the lambda role, and the policy attachment to the role:

```
resource "aws_iam_role" "lambda-role"{
    name = "lambda-role"

  assume_role_policy=<<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      }
    }
   ]
}
EOF

}
```
```
resource "aws_iam_role_policy_attachment" "LP-attach" {
    role       = "${aws_iam_role.lambda-role.name}"
    policy_arn = "${aws_iam_policy.LP.arn}"
}

```

###### Creating the Lambda function with Terraform.
Finally, I had to create the lambda function itself using Terraform:
```
resource "aws_lambda_function" "test-lambda" {
  filename         = "lambda.py.zip"
  function_name    = "my_handler"
  role             = "${aws_iam_role.lambda-role.arn}"
  handler          = "lambda.my_handler"
  source_code_hash = "${base64sha256(file("lambda.py.zip"))}"
  runtime          = "python3.6"

  vpc_config {
    subnet_ids = ["${aws_subnet.privsubnet1.id}","${aws_subnet.privsubnet2.id}"]
    security_group_ids = ["${aws_security_group.NATSG.id}"]
  }

  environment {
    variables = {
      foo = "bar"
    }
  }
```
Currently, terraform apply has to be ran, and the python code needs to be zipped, each time we want to update the code on AWS.

The Terraform for lambda should be complete at this point, but we haven't finished Docker or AWS ECR and ECS yet, so it may have to be updated again.
