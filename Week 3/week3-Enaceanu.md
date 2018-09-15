## Alex’s Blog Week 3
Divide and Conquer (my portion)
Project 1 is much more involved and requires a better divide and conquer strategy. Below are the tasks which I have been assigned or am also helping with:
Terraform Service Infrastructure - EC2 (Nat Instance)
I found terraform code examples that deploy an instance. With some minor modifications I have deployed a new instance to AWS that will act as the NAT and or bastion host. The operating system is Amazon Linux NAT. Below is the code that I used to do so:

              provider "aws" {
                region = "us-west-2"
              }

              data "aws_ami" "AmazonLinuxNAT" {
                most_recent = true

                filter {
                  name   = "name"
                  values = ["ubuntu/images/hvm-ssd/ubuntu-trusty-14.04-amd64-server]
                }

                filter {
                  name   = "virtualization-type"
                  values = ["hvm"]
                }

                owners = ["099720109477"] # Canonical
              }

              resource "aws_instance" "web" {
                ami           = "ami-40d1f038"
                instance_type = "t2.micro"

                tags {
                  Name = "NAT Instance"
                }
              }

#### Ongoing configurations
I am still working on configuring a security group for this instance as Amazon recommends in the details of documentation that I have used to work on this task. I understand that we will need to configure rules allowing traffic to our designated private subnet to and from the internet. This subnet will be the one that has the 2 blog servers running behind the load balancer.
The basic rules I will give our NAT security group are allowing inbound traffic from our designated private subnet (the source IP) over ports 80 and 443. Will likely also have traffic from the web (the source IP) allowed on port 22 (SSH). Outbound rules will be any IP 0.0.0.0 ( the destination IP) over ports 80 and 443.

Terraform Service Infrastructure - EC2 (Service instances)
I have modified the code that I used to deploy the NAT instance as detailed above to deploy an instance that runs Ubuntu Server instead. I altered the AMI selection and also the tags that I would give it for easy Identification in EC2. It is as simple as that for deploying an instance. Currently I am testing code that will assign a desired IP address for each and every instance. Below is an example of that code.

            resource "aws_network_interface" "multi-ip" {
              subnet_id   = "${aws_subnet.main.id}"
              private_ips = ["10.0.0.10", "10.0.0.11"]
            }

            resource "aws_eip" "one" {
              vpc                       = true
              network_interface         = "${aws_network_interface.multi-ip.id}"
              associate_with_private_ip = "10.0.0.10"
            }

            resource "aws_eip" "two" {
              vpc                       = true
              network_interface         = "${aws_network_interface.multi-ip.id}"
              associate_with_private_ip = "10.0.0.11"
            }
After the testing is done I will allocate an elastic IP with the code below to the NAT/bastion instance.

            resource "aws_eip" "lb" {
              instance = "${aws_instance.web.id}"
              vpc      = true
            }


Ansible: Playbook - Web server setup and configuration
No work has begun on this as of yet, I plan to install at least 2 virtual machines running Ubuntu Server and having them networked together in a test environment. One will be the host machine that will receive the software configuration from the other VM that will be the server running Ansible. This will establish a baseline for our blog server that can be deployed rapidly, favoring scalability for any potential increase in web traffic. This can be done many ways, I will look into vagrant or I may just use Microsoft Hyper V or even Oracle Virtual box. Eventually Ansible deployment will be conducted on the production environment (AWS)
#### Remaining Tasks for this weekend 
Terraform – VPC

Terraform Service Infrastructure - Everything else (joint effort)

Ansible: Playbook - Service deployment
