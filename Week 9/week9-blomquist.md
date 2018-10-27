+++
title = "Erik's Blog. Week 8."
description = "AWS Pricing Calculator"
tags = [
    "Blog",
    "beats",
    "Erik",
    "COMP 480",
    "Project 4",
]
date = "2018-10-26"
categories = [
    "Blog",
    "AWS",
]
+++

![AWS Price Calculator](https://www.hostingadvice.com/wp-content/uploads/2015/08/AWS-S3.png)

##### New AWS Pricing Calculator for EC2 and EBS

It can hard to estimate all of the costs on AWS sometimes so Amazon has developed
a NEW pricing calculator to help you estimate and understand your costs. The
new calculator can be found here: https://calculator.aws/#/

# Select Region & Add Services
1. We can start of by creating a new group, click `Add Group` in the top right corner.
2. Give the group a proper name such as `Oregon Servers` and then select `US West (Oregon)` at the bottom.
3. Next step is to add some services to estimate the cost of, click `Add Services` in the middle on the right side.
4. Click the orange button saying `Configure` under Amazon EC2.

# Quick Estimate vs Advanced Estimate
The new calculator can help us get two types of estimates, quick and advanced ones.
The quick estimate is the default option and it allows you to select and compare prices
for EC2 specifications, Pricing Strategy, and Elastic Block Storage.

The Advanced Estimate allows you to dig a little deeper into details about our costs.
It allows us to specify information about workload and data transfer.

# Pricing Models
We can find four different pricing models:

`Cost optimized` - Mix between on-demand and reserved.

`On-Demand` - Pay per hour or second

`Reserved` - Pay for reserved instances, can be a little cheaper than on-demand.

`Spot` - Marketplace for spare EC2 instances, can get up to 90% off.

# Cost optimization / Contract Terms
Amazon gives us a lot of alternatives when it comes to how to pay for the services.
A few examples of alternatives:
- 1 YR No Upfront
- 1 YR Partial Upfront
- 1 YR Full Upfront
- 1 YR No Upfront - Convertible Reserved instances
- 3 YR No Upfront
