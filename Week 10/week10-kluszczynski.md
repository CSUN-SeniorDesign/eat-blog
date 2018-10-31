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
Project 5 involves deploying our plan from last week to AWS services. Our plan involves the following steps. Getting a namecheap domain, Forwarding traffic to Route 53 name-servers. Route 53 forwards traffic to Cloudflare name-servers for www/blog/apex. Cloudflare provides a certificate, and HTML/CSS/JS caching, points to the S3 bucket. On the CI/CD side, CircleCI posts any updates from the master branch to the bucket. This is what I'll be discussing for this blog.

#### CI/CD with CircleCI
CircleCI gets ran every time there is a push to the master branch. This is setup in the .CircleCI/config.yml file with the following:

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

After this, we get into the deployment steps. First, we make a new directory, then install the necessary software to build our blog. We use hugo for our blog, so that is installed, along with dpkg to install the .deb file. Note that this is also possible with apt-get, but takes longer as it requires an "apt-get update".

```
            # Making blog upload directory
            sudo mkdir ~/blogupload
            
            # Getting required packages.
            sudo wget https://github.com/gohugoio/hugo/releases/download/v0.49/hugo_0.49_Linux-64bit.deb
            sudo apt-get install dpkg
            
            # Installing hugo
            sudo dpkg -i hugo_0.49_Linux-64bit.deb
```

Next, we set up our site, creating the new site with hugo, then moving our themes into the theme directory, and our posts into the post directory. Each theme has different requirements for where content goes, for the theme we are using (arabica), the blog posts must go in the "<sitename>/content/post" directory.

```
            # Setting up site
            cd ~/blogupload
            sudo hugo new site beats
            sudo mv -v ~/project/arabica ~/blogupload/beats/themes
            sudo mv ~/project/config.toml ~/blogupload/beats/config.toml
            sudo mkdir ~/blogupload/beats/content/post
            sudo mv -v ~/project/* ~/blogupload/beats/content/post
```

Then, we remove the leftover .deb hugo file, so it doesn't get uploaded to our site, then we build our site using hugo.

```
            # Removing deb
            sudo rm ~/blogupload/beats/content/post/hugo_0.49_Linux-64bit.deb
                        
            # Building site
            cd ~/blogupload/beats
            sudo hugo
```

After this, hugo places our completed site in a "public" directory, which contains the code required to run the site. This can be uploaded to any web server, and hosted as a website. In our case, we are using S3, because it is the cheapest option in AWS. 

Note that using the "aws s3 cp" command normally only allows one file uploaded to s3 at a time, but if you use the --recursive argument, you can upload the entire directory using just one command.  

```
    - run:   
          command: |
            # Upload files to S3
            sudo pip install awscli        
            aws s3 cp ~/blogupload/beats/public/ s3://beats480s/ --recursive

```

After all of these steps are complete, our site is uploaded to our public S3 bucket, which was previously configured as a static web host.

The site can be viewed here: http://beats480s.s3-website-us-west-2.amazonaws.com/

After this step is complete, Route53 and Cloudflare need to be set up correctly, in order to use our domain name (fa480.club).
