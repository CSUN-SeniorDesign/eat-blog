## Erik's Blog. Week 3
#### What's new this week?

##### Start of Project 1
We started Project 1 this week which involves working with Terraform & Ansible. We have been working better as a team and it has been easier to divide things among us. I was assigned the issue to create a VPC along with subnets and a internet gateway using Terraform and here is how I did it.

##### 0. Installation of Terraform and link it to AWS.
  1. Download the binary package from:
     https://www.terraform.io/downloads.html
  2. Place unzip the content into a new folder called "Terraform" under C:\
  3. cd into your new folder and type "terraform version" and you should get a similar output.

          c:\>cd C:\Terraform
          C:\Terraform>
          C:\Terraform>terraform version
          Terraform v0.11.8

  4. You now have Terraform installed!
  5. You need to link your IAM account to Terraform and you do that by open your aws cli and type "aws configure" and fill out your access key.

          $ aws configure
          AWS Access Key ID [None]: YOUR ACCESS KEY
          AWS Secret Access Key [None]:  YOUR SECRET ACCES KEY
          Default region name [None]: us-west-2
          Default output format [None]: json


##### 1. How to use Terraform to build a VPC
  1. Once Terraform has been successfully installed and linked to your aws IAM account you are ready to go. Simply create a new file in your terraform folder called "VPC.tf".
  2. Add the following code to VPC.tf and save it.

          resource "aws_vpc" "main" {
          	cidr_block = "172.31.0.0/16"
          	  tags {
          		Name = "Main-VPC"
          	}
          }

  3. Open your cmd and navigate to C:\Terraform and then type "terraform apply" and then "yes" to run all of your .tf files.

          Do you want to perform these actions?
          Terraform will perform the actions described above.
          Only 'yes' will be accepted to approve.

          Enter a value: yes
  4. You should now be able to sign in to your aws console and find a VPC there.
   ![](img/erikVPC.png?raw=true)

##### 2. How to create subnets with Terraform
   1. Here is how you create 3 public and 3 private subnets in different availability zones.

           resource "aws_subnet" "privsubnet1" {
             vpc_id     = "${aws_vpc.main.id}"
             cidr_block = "172.31.32.0/19"
             availability_zone       = "us-west-2a"
             tags {
               Name = "Privsubnet1"
             }
           }

           resource "aws_subnet" "privsubnet2" {
             vpc_id     = "${aws_vpc.main.id}"
             cidr_block = "172.31.64.0/19"
             availability_zone       = "us-west-2b"
             tags {
               Name = "Privsubnet2"
             }
           }

           resource "aws_subnet" "privsubnet3" {
             vpc_id     = "${aws_vpc.main.id}"
             cidr_block = "172.31.96.0/19"
             availability_zone       = "us-west-2c"
             tags {
               Name = "Privsubnet3"
             }
           }

           resource "aws_subnet" "pubsubnet1" {
             vpc_id     = "${aws_vpc.main.id}"
             cidr_block = "172.31.128.0/19"
             availability_zone       = "us-west-2a"
             tags {
               Name = "Pubsubnet1"
            }
           }

           resource "aws_subnet" "pubsubnet2" {
             vpc_id     = "${aws_vpc.main.id}"
             cidr_block = "172.31.160.0/19"
             availability_zone       = "us-west-2b"
             tags {
               Name = "Pubsubnet2"
             }
           }

           resource "aws_subnet" "pubsubnet3" {
             vpc_id     = "${aws_vpc.main.id}"
             cidr_block = "172.31.192.0/19"
             availability_zone       = "us-west-2c"
             tags {
               Name = "Pubsubnet3"
             }
           }

##### 3. How to create an Internet Gateway
          resource "aws_internet_gateway" "gw" {
            vpc_id = "${aws_vpc.main.id}"
          }

#### What to do next week?
We are planning to finish the Terraform tasks over the weekend so that we have enough of time to spend on the tasks for Ansible, Deliverables and our Presentation.
