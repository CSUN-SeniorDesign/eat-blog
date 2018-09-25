## Tyler's Blog. Week 3
#### What's new this week?

###### Starting project 1
Project 1 is much more organized than Project 0 was. Each team member is assigned their own set of tasks to work on.
Here are my issues:
* Terraform - IAM
* Improving GitHub instructions
* Terraform - Load Balancers
* Terraform - Route 53

This blog, I'll cover the process I used to set up IAM using terraform.

###### Learning terraform and AWS CLI
Before Project 1, I had no experience with Terraform or AWS CLI, so I had to learn everything from the ground up. I was also the first person in my group to start using Terraform, so I couldn't rely on my other group members for help.

###### Starting terraform IAM
On Monday, I had to learn terraform to set up IAM users so the rest of our group could start working on other parts of the project. By around 8pm on Monday, I had IAM set up to the specifications of the project, with no experience writing any terraform code before.

###### The Terraform Code
The following is the terraform code I wrote on Monday to set up the AWS IAM.

```
provider "aws" {
  region     = "us-west-2"
}

resource "aws_iam_group" "Eat-Team" {
  name = "EAT-Team"
}

resource "aws_iam_user" "Alex"{
  name = "Alex"
}

resource "aws_iam_user" "Erik"{
  name = "Erik"
}

resource "aws_iam_user" "TK"{
  name = "TK"
}

resource "aws_iam_user" "Brian"{
  name = "Brian"
}

resource "aws_iam_group_membership" "EAT-Membership" {
  name = "Adding-members-to-EAT"

  users = [
    "${aws_iam_user.Alex.name}",
    "${aws_iam_user.Erik.name}",
	"${aws_iam_user.Brian.name}",
	"${aws_iam_user.TK.name}",
  ]

  group = "${aws_iam_group.Eat-Team.name}"
}

data "aws_iam_policy" "policy" {
  arn = "arn:aws:iam::aws:policy/AdministratorAccess"
}

resource "aws_iam_group_policy_attachment" "attach-policy" {
  group = "${aws_iam_group.Eat-Team.name}"
  policy_arn = "${data.aws_iam_policy.policy.arn}"
}
```

###### Code Breakdown
First, the provider is specified, AWS using the us-west-2 region (Oregon):
```
provider "aws" {
  region     = "us-west-2"
}
```

Next, a group is created named "Eat-Team":

```
resource "aws_iam_group" "Eat-Team" {
  name = "EAT-Team"
}
```

Third, four users are created.
```
resource "aws_iam_user" "Alex"{
  name = "Alex"
}

resource "aws_iam_user" "Erik"{
  name = "Erik"
}

resource "aws_iam_user" "TK"{
  name = "TK"
}

resource "aws_iam_user" "Brian"{
  name = "Brian"
}
```
Next, all four users are added to the Eat-Team group.

```
resource "aws_iam_group_membership" "EAT-Membership" {
  name = "Adding-members-to-EAT"

  users = [
    "${aws_iam_user.Alex.name}",
    "${aws_iam_user.Erik.name}",
	"${aws_iam_user.Brian.name}",
	"${aws_iam_user.TK.name}",
  ]

  group = "${aws_iam_group.Eat-Team.name}"
}
```
Note the syntax for Terraform variables. It took a while to completely understand how the syntax works.

First is the name (class) of the resource, followed by the 'instance' of the resource, then the 'instance attribute' to access. (I am not sure on the wording here, but it seems very similar to object-oriented programming.)

Finally we create a policy, and attach admin rights to the policy, then we attach the policy to the Eat-Team group.
```
data "aws_iam_policy" "policy" {
  arn = "arn:aws:iam::aws:policy/AdministratorAccess"
}

resource "aws_iam_group_policy_attachment" "attach-policy" {
  group = "${aws_iam_group.Eat-Team.name}"
  policy_arn = "${data.aws_iam_policy.policy.arn}"
}
```
Note that the policy/AdministratorAccess is an AWS built-in policy.

Here we can also see syntax for 'data' fields opposed to 'resource' fields. When data instances are accessed, it is required to put 'data.' before the name of the resource.

###### This weekend and next week's plans
It seems like we are quite behind schedule, as we don't have the EC2 instances up and running completely. This will need to be finished over the weekend, along with route-tables, the application load balancer and Route 53.

We will hopefully have next week to work just on Ansible, the deliverables, and the presentation.
