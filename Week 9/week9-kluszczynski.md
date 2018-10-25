+++ 
title = "Tyler's Blog. Week 9." 
description = "Project 4" 
tags = [ 
    "Blog", "beats", "Tyler", "CIT 480",
] 
date = "2018-10-25" 
categories = [ 
    "Blog",
] 
menu = "main" 
+++

## Tyler's Blog. Week 8.
#### What's new this week?

#### Project 4
Project 4 was much more simple than the other projects, and involved more research than hands-on. I did mostly all of the research for the project, as it isn't something that can easily be split up. For this blog, I will cover my journey through researching the least expensive way to host a site on AWS.

#### S3
S3 is the go-to solution when thinking about cheap web hosting. It only costs a couple cents to host files in an S3 bucket, which is much cheaper than what can reasonably expected through anything else. Doing the calculations for 30,000 monthly page hits leads to a cost of close to $0.40 for data transfer. The largest costs for hosting a website will be data transfer and Route 53 integration. 

##### Limiting Data Transfer Costs
There is a way to limit the AWS data transfer cost, which involves using a third party for website caching, for example Cloudflare, which is quite popular. Cloudflare will cache your html, css, and javascript so it doesn't have to be fetched from S3 each time a user wants to access your website. It also offers other benefits, such as serving cached web pages even if your site is offline, all for free.

##### Limiting Route 53 Costs
This project requires Route 53 to be used, but in a production environment, it is possible to use your name provider (e.g. namecheap) to act as a DNS provider, which will eliminate the Route 53 charges.

#### Increase in Data Out
If we were to see an increase in data out, past around 20-50GB, prices will increase dramatically. In these cases, using Cloudflare would be much more important, as well as considering other options, such as LightSail which provides small EC2 instances along with free data-out transfer, for around $3.50 a month. 
