+++ 
title = "Tyler's Blog. Week 10." 
description = "Project 5" 
tags = [ 
    "Blog", "beats", "Tyler", "CIT 480",
] 
date = "2018-10-31" 
categories = [ 
    "Blog",
] 
menu = "main" 
+++

#### What's new this week?

#### Project 5
Project 5 involves deploying our plan from last week to AWS services. Our plan involves the following steps. Getting a namecheap domain, Forwarding traffic to Route 53 nameservers. Route 53 forwards traffic to Cloudflare nameservers for www/blog/apex. Cloudflare provides a certificate, and HTML/CSS/JS caching, points to the S3 bucket. On the CI/CD side, CircleCI posts any updates from the master branch to the bucket. This is what I'll be discussing for this blog.

#### CI/CD with CircleCI
CircleCI gets ran everytime there is a push to the master branch. This is setup in the .circleci/config.yml file with the following:

```
version: 2
jobs:
  build:
    branches:
      only:
        - master
```

We are using CircleCI's Ubuntu machine, instead of a container image:

```
 machine: true
```

After this, we get into the deployment steps. Frst, we make a new driectory, then install the necessary software to build our blog.

```
            # Making blog upload directory
            sudo mkdir ~/blogupload
            
            # Getting required packages.
            sudo wget https://github.com/gohugoio/hugo/releases/download/v0.49/hugo_0.49_Linux-64bit.deb
            sudo apt-get install dpkg
            
            # Installing hugo
            sudo dpkg -i hugo_0.49_Linux-64bit.deb
```

Next, we set up our site, creating the new site with hugo, then moving our themes into the theme directory, and our posts into the post directory.

```
            # Setting up site
            cd ~/blogupload
            sudo hugo new site beats
            sudo mv -v ~/project/arabica ~/blogupload/beats/themes
            sudo mv ~/project/config.toml ~/blogupload/beats/config.toml
            sudo mkdir ~/blogupload/beats/content/post
            sudo mv -v ~/project/* ~/blogupload/beats/content/post
```

Then, we remove the leftover .deb hugo file, so it doesn't get uploaded to our site, and we build our site.

```
            # Removing deb
            sudo rm ~/blogupload/beats/content/post/hugo_0.49_Linux-64bit.deb
                        
            # Building site
            cd ~/blogupload/beats
            sudo hugo
```

After this, hugo places our site in a "public" directory. This is what gets uploaded to our S3 bucket.

```
    - run:   
          command: |
            # Upload files to S3
            sudo pip install awscli        
            aws s3 cp ~/blogupload/beats/public/ s3://beats480s/ --recursive

```

After all of these steps are complete, our site is uploaded to our public S3 bucket, which was preeviously configured as a static web host.

The site can be viewed here: http://beats480s.s3-website-us-west-2.amazonaws.com/
After this step is complete, Route53 and Cloudflare need to be set up correctly, in order to use our domain name (fa480.club).


