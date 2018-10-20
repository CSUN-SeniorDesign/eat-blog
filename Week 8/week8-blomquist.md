+++
title = "Erik's Blog. Week 8."
description = "Amazon Elastic Container Services (ECS) and Elastic Container Registry (ECR) - Part 2 of 2"
tags = [
    "Blog",
    "beats",
    "Erik",
    "COMP 480",
    "Project 3",
]
date = "2018-10-19"
categories = [
    "Blog",
    "AWS",
]
menu = "main"
+++

![AWS logo](https://cgnet.com/wp-content/uploads/aws.png)

Last weeks blog went over how to setup ECS: Roles & Policies, Cluster and ECR.
This week will finish up this project so it will cover the following:
- EC2 Host
- ECS Auto Scaling Group
- ECS Tasks
- ECS Services
- ECS ALB

##### ECS - EC2 Host
We need to create a launch-configuration that uses an ECS optimized AMI so that
our EC2 can host our containers.

```
resource "aws_launch_configuration" "ecs-launch-configuration" {
  name_prefix           = "ecs-cluster-launch"
  image_id              = "ami-00430184c7bb49914"
  security_groups       = ["${aws_security_group.NATSG.id}"]
  instance_type         = "t2.micro"
  key_name              = "${aws_key_pair.deployer.key_name}"
  iam_instance_profile  = "${aws_iam_instance_profile.ecs-instance-profile.id}"
  user_data             = "#!/bin/bash\necho 'ECS_CLUSTER=beats-cluster' > /etc/ecs/ecs.config\nstart ecs"
root_block_device {
  volume_type = "standard"
  volume_size = 8
  delete_on_termination = true
}

lifecycle {
  create_before_destroy = true
}
  associate_public_ip_address = "false"
}
```

*Warning!*
I included *name = "beats"* at the top but our volume sizes ended up being 100 GB each.

##### ECS - Auto Scaling Group
Our Auto Scaling Group will use the launch-configuration we created in the previous
step and start x-amount of instances, 2 in this case (depending on desired_capacity "x").
```
# ECS ASG
resource "aws_autoscaling_group" "ecs-autoscaling-group" {
  name = "ecs-autoscaling-group"
  max_size = "2"
  min_size = "1"
  desired_capacity = "2"
  vpc_zone_identifier = ["${aws_subnet.privsubnet1.id}"]
  launch_configuration = "${aws_launch_configuration.ecs-launch-configuration.name}"
  health_check_type = "ELB"
  target_group_arns = ["${aws_alb_target_group.production-HTTP-Group.arn}"]
tag {
  key = "Name"
  value = "-beats-ecs-asg"
  propagate_at_launch = true
}
}
```
### ECS Tasks
We are now going to declare tasks that our containers in the cluster can use. Create a new file called `ECS-tasks.tf`.

```
resource "aws_ecs_task_definition" "beats-staging" {
  family                = "beats-staging"
  container_definitions = "${file("task-definitions/staging.json")}"
  volume {
    name      = "beats-staging"
    host_path = "/ecs/beats_service"
  }
  placement_constraints {
    type       = "memberOf"
    expression = "attribute:ecs.availability-zone in [us-west-2a, us-west-2b]"
  }
}

resource "aws_ecs_task_definition" "beats-production" {
  family                = "beats-production"
  container_definitions = "${file("task-definitions/production.json")}"
  volume {
    name      = "beats-production"
    host_path = "/ecs/beats_service"
  }

  placement_constraints {
    type       = "memberOf"
    expression = "attribute:ecs.availability-zone in [us-west-2a, us-west-2b]"
  }
}
```

Create a new folder called `task-definitions` inside your project folder and then create 2 new files called `staging.json` and `production.json`. No need to specify the image since it will be pulled from the ECR later with Lambda.

*staging.json*
```
[
  {
    "name": "beats-staging",
    "image": "service-first",
    "cpu": 10,
    "memory": 512,
    "essential": true,
    "portMappings": [
      {
        "containerPort": 80,
        "hostPort": 80
      }
    ]
  }
]
```
*production.json*
```
[
  {
    "name": "beats-production",
    "image": "service-first",
    "cpu": 10,
    "memory": 512,
    "essential": true,
    "portMappings": [
      {
        "containerPort": 80,
        "hostPort": 80
      }
    ]
  }
]
```

##### ECS Services
We now need Services so that we can use our tasks in the cluster.
```
# ECS Services
## beats-staging task
resource "aws_ecs_service" "beats-staging" {
  name            = "beats-staging"
  cluster         = "${aws_ecs_cluster.beats-cluster.id}"
  task_definition = "${aws_ecs_task_definition.beats-staging.arn}"

  load_balancer {
    target_group_arn = "${aws_alb_target_group.staging-HTTP-Group.arn}"
    container_name   = "beats-staging"
    container_port   = 80
  }

  placement_constraints {
    type       = "memberOf"
    expression = "attribute:ecs.availability-zone in [us-west-2a, us-west-2b]"
  }
}

# beats-production task
resource "aws_ecs_service" "beats-production" {
  name            = "beats-production"
  cluster         = "${aws_ecs_cluster.beats-cluster.id}"
  task_definition = "${aws_ecs_task_definition.beats-production.arn}"

  load_balancer {
    target_group_arn = "${aws_alb_target_group.production-HTTP-Group.arn}"
    container_name   = "beats-production"
    container_port   = 80
  }

  placement_constraints {
    type       = "memberOf"
    expression = "attribute:ecs.availability-zone in [us-west-2a, us-west-2b]"
    }

}

```

##### ECS ALB
We can still use our old load balancer found in `Services.tf` but we need to do some adjustments.

```
resource "aws_lb" "Load-Balancer"{
  name               = "Load-Balancer"
  internal           = false
  load_balancer_type = "application"
  security_groups = ["${aws_security_group.NATSG.id}"]
  enable_cross_zone_load_balancing = true
  enable_deletion_protection = false

  subnets            = ["${aws_subnet.pubsubnet1.id}","${aws_subnet.pubsubnet2.id}","${aws_subnet.pubsubnet3.id}"]
}

resource "aws_alb_listener" "HTTP-Listener"{
	load_balancer_arn = "${aws_lb.Load-Balancer.id}"
	port = 80
	default_action {
		type = "redirect"
    redirect {
      port = "443"
      protocol = "HTTPS"
      status_code = "HTTP_301"
    }
	}
}

resource "aws_alb_listener" "HTTPS-Listener"{
	load_balancer_arn = "${aws_lb.Load-Balancer.id}"
	port = "443"
  protocol = "HTTPS"
	ssl_policy = "ELBSecurityPolicy-2016-08"
	certificate_arn = "${aws_acm_certificate.cert.arn}"
	default_action {
		type = "forward"
		target_group_arn = "${aws_alb_target_group.production-HTTP-Group.arn}"
	}
}
```

We need to edit our old HTTP-Group and create a new one like this:
```
resource "aws_alb_target_group" "staging-HTTP-Group" {
  name     = "staging-HTTP-Group"
  port     = 80
  protocol = "HTTP"
  vpc_id   = "${aws_vpc.main.id}"
  depends_on = ["aws_lb.Load-Balancer"]
}

resource "aws_alb_target_group" "production-HTTP-Group" {
  name     = "production-HTTP-Group"
  port     = 80
  protocol = "HTTP"
  vpc_id   = "${aws_vpc.main.id}"
  depends_on = ["aws_lb.Load-Balancer"]
}

resource "aws_lb_listener_rule" "beats-staging" {
  listener_arn = "${aws_alb_listener.HTTPS-Listener.arn}"
  priority = 10
  action = {
    type = "forward"
    target_group_arn = "${aws_alb_target_group.staging-HTTP-Group.id}"
  }
  condition = {
    field = "host-header"
    values = ["*staging.fa480.club"]
  }
}

```
Yaaaay, you're done. Come back next week!
