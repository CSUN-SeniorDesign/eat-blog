## Alex’s Blog Week 3

####Continuation of Project 1

There was still a lot of work to do with Terraform and Ansible, plus of course
the many issues that arose. We got a new addition to the team and decided to
delegate Ansible tasks to him. Luckily, last week I learned a lot about Terraform
by writing and testing code for the NAT/Bastion and blog server instances. I also
reviewed a lot of different example code, from Terraforms website which is very
helpful especially with regards to modifying code with arguments. Also the
proper use of interpolation was
something I originally missed, figuring that out made the scripting potential
more robust. After that the NAT instance code was cut down to these few lines
with the desired arguments that place our NAT instance in its proper location:

    resource "aws_instance" "NAT" {
    ami           = "ami-40d1f038"
     instance_type = "t2.micro"
     subnet_id = "${aws_subnet.pubsubnet1.id}"
     associate_public_ip_address = true
     vpc_security_group_ids = ["${aws_security_group.NATSG.id}"]
	   key_name = "${aws_key_pair.deployer.key_name}"
    tags {
       Name = "NAT Instance"
      }
    }

Once this script was validated as working, the same refinement was applied to
blog server instances which are deployed with similar code, except that code
specifies that the servers to spawn in a private subnet with a different security
group. We also had to distribute a key pair to each instance for authentication.
This was accomplished with the "key_name" argument.

####Security groups

With my new found yet minimal terraform skills I shifted to researching security
groups. I decided to start by drawing the network diagram, something the team
and I have decided to  do at the beginning of each project from now on. After
the diagram was drawn, I was able to visualize the VPC better and especially
analyze the flow of traffic better.

Here is the code that I used to confiugre the the security group for the
NAT/Bastion instance:

    resource "aws_security_group" "NATSG" {
    name        = "NATSG"
    description = "NAT_security_group"
    vpc_id      = "${aws_vpc.main.id}"

    ingress {
    description = "Allow inbound HTTP traffic."
      from_port   = 80
      to_port     = 80
      protocol    = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
    }

    ingress {
    description = "Allow inbound HTTPS traffic"
      from_port   = 443
      to_port     = 443
      protocol    = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
    }

    ingress {
    description = "Allow inbound SSH access"
      from_port   = 22
      to_port     = 22
      protocol    = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
    }

    egress {
    description = "Allow outbound SSH access"
     from_port    = 22
     to_port      = 22
     protocol     = "tcp"
     cidr_blocks  = ["0.0.0.0/0"]
    }

    egress {
    description = "Allow outbound HTTP access to the Internet"
      from_port    = 80
      to_port      = 80
      protocol     = "tcp"
      cidr_blocks  = ["0.0.0.0/0"]
    }

    egress {
    description = "Allow outbound HTTPS access to the Internet"
      from_port    = 443
      to_port      = 443
      protocol     = "tcp"
      cidr_blocks  = ["0.0.0.0/0"]
      }
    }

As you can see, this code is very straight forward. The important part is
specifying the ports and source and destination IP addresses. I recommend
adding a description for each inbound and outbound rule so that it displays in
the AWS console.
Once I verified this code was working, the same process was followed for the
Blog security group. The rules are different for this group since TLS/SSL
decryption occurs at the application load balancer in the public subnet.
Therefore there is no need for port 443 to be open as seen in the code below:

      resource "aws_security_group" "BlogSG"{
      name = "BlogSG"
	     description = "Blog security group"
	      vpc_id = "${aws_vpc.main.id}"

        ingress {
        description = "Allow SSH traffic"
		     from_port     = 22
		     to_port       = 22
		     protocol      = "tcp"
		     cidr_blocks   = ["0.0.0.0/0"]
	      }

        egress {
        description = "Allow SSH traffic"
		      from_port     = 22
		      to_port       = 22
		      protocol      = "tcp"
		      cidr_blocks   = ["0.0.0.0/0"]
	      }

        ingress {
        description = "Allow HTTP traffic from pubsubnet1"
		      from_port     = 80
		      to_port       = 80
		      protocol      = "tcp"
		      cidr_blocks   = ["172.31.128.0/19"]
	      }

        egress {
        description = "Allow HTTP traffic to pubsubnet1"
		     from_port     = 80
		     to_port       = 80
		     protocol      = "tcp"
		     cidr_blocks   = ["172.31.128.0/19"]
	      }
      }

After the code was validated and the team got some state locking issues fixed,
we blew away our entire VPC and ran all our refined terraform code together and
we ere happy to see everything worked out. We then manually SSH'ed into our
NAT/Bastion instance since it is the secure entry point to our network, and
subsequently into our bog servers. Achieving this required a slightly different
configuration for me since I use putty to connect to our instances. I had to use
pageant to add the key we use instead of adding it for each session. I also had
to select, agent forwarding so that the key can be used for authenticating our
connection to the blog servers as well. Once this all worked, it showed us that
our networking and security groups were set up properly. This meant that the
production environment was ready for configuration and deployment of software
and our blog via Ansible!
