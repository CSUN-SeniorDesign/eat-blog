## Erik's Blog. Week 6.
I was assigned the **HashiCorp Packer** task for Project 2 where I created a base AMI from one single source configuration to be used on our web servers. Below are a few problems that I ran into.

##### Exporting Files to Packer
I ran into some issues during this project where I was unable to run scripts properly. I did not understand at first that you can export files from your local computer into Packer so I tried to create my own scripts. Here is how I solved it by using provisioners to import files onto my base AMI with Packer.
````
{
"type": "file",
"source": "staging/blog.staging.fa480.club.conf",
"destination": "/home/ubuntu/blog.staging.fa480.club.conf"
},
````
In the example above, we are exporting a file from our local machine which I have declared under type and the file is called `blog.staging.fa480.club.conf` and it is located in the `staging/` folder of my projects folder (locally). The destination of my file is the `/home/ubuntu/` folder, remember to include the file extensions of the file when you declare the destination.

You should now be able to export files such as scripts onto your AMI.

##### "Waiting for SSH..."
Another problem that I ran into was that my packer builds would get stuck on "Waiting for SSH..." and then timed-out and terminated itself. I found it hard to troubleshoot this problem because it was not so much documentation about it. However, the problem was that I did not declare our bastion host in packer properly. Adding the following solved the problem for me.

1. SSH for Bastion/NAT
Before being able to deploy things in our private subnet we need to have access SSH through our Bastion/NAT.
````
"ssh_bastion_host": "34.213.12.211",
"ssh_bastion_username": "ec2-user",
"ssh_bastion_private_key_file": "privatekey.pem",
````

2. SSH private key
This is the lines I added to allow SSH onto our newly created AMI for testing in debug mode.
````
"ssh_keypair_name": "deployer-key",
"ssh_private_key_file": "privatekey.pem",
"ssh_username": "ubuntu",
"ssh_pty": "true",
````
3. IAM credentials
Packer was unable to read the proper AWS credentials but I did some digging and found out that the credentials can be read from your local AWS configuration.
````
"access_key": "{{user `aws_access_key`}}",
"secret_key": "{{user `aws_secret_key`}}",
````
