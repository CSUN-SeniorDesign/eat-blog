+++ title = "Shahid's Blog. Week 6" date = "2018-10-05" +++
## Shahid's Blog. Week 6
#### What's new this week?

##### Why use terraform
Terraform is an automation tool to create infrastructure using code rather than manually
downloading and installing software. In order to fully test software, production environments are often cloned and used as a staging environment for testing.

##### Installing and using terraform on Ubuntu 14.04 64-bit
1. Visit https://www.terraform.io/
2. Click on downloads or go to https://www.terraform.io/downloads.html
3. Click on the Linux 64-bit link and the download will start.
4. Once the download is finished, unzip the file.
5. Move the executable into /usr/local/bin
6. Test that the installation was successful by opening up a terminal and typing ```terraform```

##### Using terraform on Ubuntu 14.04 64-bit
The files that terraform looks for are called configuration files and end in the .tf file extension.

  /path/to/folder/
  - services.tf
  - iam-roles.tf
  - s3-bucket.tf

Logical separation of goals should be done through multiple configuration files much like how code is separated into functions/methods and across files depending on what it does.

The syntax for terraform is in JSON:
```
  resource "aws_launch_configuration" "launch-config"{
  image_id = "ami-0347d2b486d3bc83e"
  instance_type = "t2.micro"
  security_groups = ["${aws_security_group.NATSG.id}"]
  ebs_optimized = false
  key_name = "${aws_key_pair.deployer.key_name}"
  iam_instance_profile = "${aws_iam_instance_profile.IP.arn}"

  lifecycle {
    create_before_destroy = true
  }
}
```

```Resource ...``` is a label for a function that terraform will carry out.
Everything below that will be options that customized how the function will be run.

Once the configuration files you want are ready, terraform will need to be initialized for the very first time. Please note you must run this command only this once: ```terraform init```

Finally in order to run your configuration all that's left is to type ```terraform apply```

All the configuration files will be ran and the output displayed on what has been added, changed, or destroyed to/from the environment.
