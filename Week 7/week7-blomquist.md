+++
title = "Erik's Blog. Week 7."
description = "Get Started with Amazon Elastic Container Services (ECS) and Elastic Container Registry (ECR)- Part 1"
tags = [
    "Blog",
    "beats",
    "Erik",
    "COMP 480",
]
date = "2018-10-12"
categories = [
    "Blog",
]
menu = "main"
+++

## Erik's Blog. Week 7.
![Image of ECS](https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTkDmRW5CPrryBo5tXGKkph0g51bFkO4qsmDYaXFDQmMEeLWvkVsA)
#### Get Started with Amazon Elastic Container Services (ECS) and Elastic Container Registry (ECR)- Part 1
ECS allows you run and scale containerized applications on AWS such as Docker. We are basically going to create a cluster where we create an EC2 instance that can run our containers with the help of tasks that allows us to define our docker image and what resources it needs. We are also going to use services to tell ECS which cluster to run our applications on.

##### ECS Roles & Policies
The first step for us is to create the roles and policies needed for our ECS service.

1. Create a new file called `ecs-roles.tf` and put the following inside:

```
resource "aws_iam_role" "ecs-instance-role" {
  name = "ecs-instance-role"
  path = "/"
  assume_role_policy = "${data.aws_iam_policy_document.ecs-instance-policy.json}"
}

data "aws_iam_policy_document" "ecs-instance-policy" {
  statement {
  actions = ["sts:AssumeRole"]
principals {
  type = "Service"
  identifiers = ["ec2.amazonaws.com"]
}
}
}

resource "aws_iam_role_policy_attachment" "ecs-instance-role-attachment" {
  role = "${aws_iam_role.ecs-instance-role.name}"
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonEC2ContainerServiceforEC2Role"
}

resource "aws_iam_instance_profile" "ecs-instance-profile" {
  name = "ecs-instance-profile"
  path = "/"
  role = "${aws_iam_role.ecs-instance-role.id}"
  provisioner "local-exec" {
  command = "sleep 60"
}
}

resource "aws_iam_role" "ecs-service-role" {
  name = "ecs-service-role"
  path = "/"
  assume_role_policy = "${data.aws_iam_policy_document.ecs-service-policy.json}"
}

resource "aws_iam_role_policy_attachment" "ecs-service-role-attachment" {
  role = "${aws_iam_role.ecs-service-role.name}"
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonEC2ContainerServiceRole"
}

data "aws_iam_policy_document" "ecs-service-policy" {
  statement {
  actions = ["sts:AssumeRole"]
principals {
  type = "Service"
  identifiers = ["ecs.amazonaws.com"]
}
}
}
```
  2. Save your file next to your other Terraform files and `cd` into that directory and run:

```
  terraform init
  terraform plan
```

  3. If everything looks good, run:

```
  terraform apply
```

  4. The roles and policies are now created!

##### Elastic Container Services (ECS) cluster with Terraform
  1. Create a new file called `ecs.tf` and place it in the same folder as `ecs-roles.tf`.
  2. Place the following content inside your newly created file.

```
# Create Cluster
resource "aws_ecs_cluster" "beats-cluster" {
    name = "beats-cluster"
}
```

  3. The code above creates a new ECS cluster called `beats-cluster`. You can now login to your AWS console and click `Elastic Container Services` to see your new cluster at the bottom.

##### Elastic Container Registry (ECR) with Terraform
The ECR is a repository where we can store our images created in Docker. To do so we first need to create our ECR.
  1. Create a new file in the same folder as before and call it `ecr.tf`.
  2. Copy and paste the code below:

```
  # Create ECR
  resource "aws_ecr_repository" "beats_repo" {
    name = "beats_repo"
  }

  # Output URL
  output "beats-repository-URL" {
    value = "${aws_ecr_repository.beats_repo.repository_url}"
  }
```

  3. The first code block creates our ecr reposiotry and calls it `beats_repo`. The second block is used to output the URL to our repository so we do not have to logon to the AWS console to find it.
  4. Open your terminal and run terraform again to start your ECR and ECS.

```
    terraform plan
    terraforn apply
```
  5. If you login to your AWS console and then click on `Elastic Container Services` and then `Clusters` you will find your cluster at the bottom of the page. You can click on the title to find more information.
  6. You can click `Repositories` on the left side under Amazon ECR to find information about your Container Registry. You should have one repository there already called `beats_repo`.

##### Next Week - Part 2
I will demonstrate how to setup our EC2 instance that will host our containers and I will define our ECS tasks and services next week once our image are available.
