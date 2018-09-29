## Alex's Blog. Week 5
#### Project 2 begins
This week we finsined project 1 Monday morning with a presentation and a frew last minute changes. Project 2 began right after. Luckily, we get to start with five members from the get go. This project builds on last week and involves several new technologies such as CircleCI, Datadog and Packer.

##### Starting Datadog
For Datadog, there are various ways to approach the requirements. We will need to gather a multitude of metrics such as CPU and memory usage. Datadog makes this process relatively easy through their integrations console. However, for this to work, Datadog agent must be installed on the target machines. For Amazon Linux, which our NAT instance runs. We used the following command:

    DD_UPGRADE=true bash -c "$(curl -L https://raw/Datadog/Datadog-agent/master/cmd/agent/install_script.sh)"

This needs to be done via ansible and all Ansible will really do is run this command. Once the Datadog agent is installed on the target machine(s). We can configure the dashboard, but we will still need to grant Datadog access to the AWS environment. To accomplish this I initially tried by creating a new IAM user and policy to attach to the user with the following code:



    resource "aws_iam_group" "3rd-Party" {
    name = "3rd-Party"
    }

    resource "aws_iam_user" "Datadog"{
      name = "Datadog"
    }

    resource "aws_iam_group_membership" "3rd-Party-Membership" {
      name = "Adding-members-to-3rd-Party"

      users = ["${aws_iam_user.Datadog.name}"]

      group = "${aws_iam_group.3rd-Party.name}"
    }

    data "aws_iam_policy" "3rd-party-policy" {
      arn = "arn:aws:iam::aws:policy/ReadOnlyAccess"
    }

    resource "aws_iam_group_policy_attachment" "attach-policy-ReadOnlyAccess" {
      group = "${aws_iam_group.3rd-Party.name}"
      policy_arn = "${data.aws_iam_policy.3rd-party-policy.arn}"
    }

The above code worked without issue, however, further investigation revealed that an AWS IAM role is required instead of an IAM user. Luckily, we can apply a policy to an IAM role so we can reuse that portion of the above code.  An IAM role can be coded in Terraform with the following:

        resource "aws_iam_role" "test_role" {
          name = "test_role"

          assume_role_policy = <<EOF
        {
          "Version": "2012-10-17",
          "Statement": [
        {
          "Action": "sts:AssumeRole",
          "Principal": {
          "Service": "ec2.amazonaws.com"
        },
        "Effect": "Allow",
        "Sid": ""
        }
      ]
    }
    EOF
    }

In this example, we designate the use of an IAM role policy with the assume_role_policy argument, which is slightly different than a standard IAM policy. This same method can be used to create a role for other services, such as packer. A least privileged model can be applied via the specifications in the policy.

#### Coming up . . .
Before we continue with Datadog, we have to get packer working first in order to create a base AMI of our blog servers and then spawn multiple instances via the auto scaling group function, which is near completion. Most of this work will be done after this blog is due via collaboration software. The issue has been getting access to our base ami that is created with packer. 
