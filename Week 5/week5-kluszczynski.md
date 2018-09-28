## Tyler's Blog. Week 4
#### What's new this week?

##### Starting Project 2
Project 2 is much more organized than project 1 was, but I still feel like we can make some improvements for next project. Also I believe that the work is getting slightly more balanced out (it helps that we have 5 people.)

Speaking of work, one of my task for this project this week was setting up CircleCI, which was completed Thursday in class. This is quite a large milestone for the project as it is around 15% of the requirements.


##### CircleCI - Starting
When I started setting up CircleCI, I accidently pushed it into the infrastructure repo, which had to be undone. This wasn't a major problem but it will show a theme in this week's task: uploading to Github.

As CircleCI will only run a build after it has been uploaded to GitHub, I had to create my own branch to upload the config.yml to whenever I was testing. As a result, I believe our blog repo has gained 30-50 commits.

##### Code Review: The Config File

I am planning on adding a section to my blog called "Code Review" where I will discuss the code that I wrote in the past week (assuming I receive a task that requires me to code).

Here is the entirity of the config file:
```
version: 2
jobs:
  build:
    machine: true
    steps:
      - checkout
      - run:
          command: |
            sudo mkdir ~/blogtozip    
      - run:   
          command: |
            # This way allows you to install hugo with snapd. Takes longer but automatically updated.
            #sudo apt-get update
            #sudo apt-get install -y snapd
            #sudo snap install hugo
            # This way allows dpkg with a .deb release (will have to be manually updated)
            sudo wget https://github.com/gohugoio/hugo/releases/download/v0.49/hugo_0.49_Linux-64bit.deb
            sudo apt-get install dpkg
            sudo dpkg -i hugo_0.49_Linux-64bit.deb
      - run:   
          command: |
            cd ~/blogtozip
            sudo hugo new site beats
            sudo mv -v ~/project/hugo-theme-dream-master/ ~/blogtozip/beats/themes/
            sudo mv ~/project/config.toml ~/blogtozip/beats/config.toml
            sudo mv -v /home/circleci/project/* /home/circleci/blogtozip/beats/content
      - run:   
          command: |
            cd ~/blogtozip/beats
            sudo hugo
      - run:
          command : |
            cd ~/blogtozip/beats
            pwd
            ls
            sudo rm public/hugo_0.49_Linux-64bit.deb
            sudo tar -zcvf $CIRCLE_SHA1.tar.gz public/  
      - run:
         command: sudo pip install awscli
      - run:
         command: |
           cd ~/blogtozip/beats
           aws s3 cp $CIRCLE_SHA1.tar.gz s3://csuneat-project-2/Uploads/

```
The most resent version of the config.yml file can be found on our master branch [here](https://github.com/CSUN-SeniorDesign/eat-blog/blob/master/.circleci/config.yml) as well.

###### Code Review: Build
I am only using one job for the entire build, so we will progress straight onto the build section.

For the build, instead of running a docker image, I chose to run a "machine," which is basically an Ubuntu virtual machine opposed to a container. Note that this option may require an additional fee in future updates (as per [here](https://circleci.com/docs/2.0/executor-types/)).

The ubuntu VM has numerous advantages compared to a docker image (Full root access), but it does take longer to load and get up and running. In an environment where speed of updates is critical, this option might not be as good.
```
build:
    machine: true
    steps:   
```
###### Code Review: Steps

The steps I used are a series of commands. Basically, the entire config is a bash file, with the checkout step.


```
steps:
      - checkout
      - run:
          command: |
            sudo mkdir ~/blogtozip    
```

When I first started experimenting with installing Hugo on the machine, I was using snap (like we used for our servers in Project 1 with Ansible). Unfortunately, the version of the machine isn't completely updated, so it's not possible to install snapd without getting an update. This update takes around 3-4 minutes of additional processing time.

I decided to come up with another solution to save build time, using wget on the latest build, then installing dpkg, and installing Hugo through the .deb package.

```
      - run:   
          command: |
            # This way allows you to install hugo with snapd. Takes longer but automatically updated.
            #sudo apt-get update
            #sudo apt-get install -y snapd
            #sudo snap install hugo
            # This way allows dpkg with a .deb release (will have to be manually updated)
            sudo wget https://github.com/gohugoio/hugo/releases/download/v0.49/hugo_0.49_Linux-64bit.deb
            sudo apt-get install dpkg
            sudo dpkg -i hugo_0.49_Linux-64bit.deb
```
From there, most of the code is self-explanatory until the end.
```
      - run:   
          command: |
            cd ~/blogtozip
            sudo hugo new site beats
            sudo mv -v ~/project/hugo-theme-dream-master/ ~/blogtozip/beats/themes/
            sudo mv ~/project/config.toml ~/blogtozip/beats/config.toml
            sudo mv -v /home/circleci/project/* /home/circleci/blogtozip/beats/content
      - run:   
          command: |
            cd ~/blogtozip/beats
            sudo hugo
      - run:
          command : |
            cd ~/blogtozip/beats
            pwd
            ls
            sudo rm public/hugo_0.49_Linux-64bit.deb
            sudo tar -zcvf $CIRCLE_SHA1.tar.gz public/  
```
The AWS CLI needs to be installed in order to upload to our S3 bucket. As a result, we have to sign into AWS, but we can't do that using "aws configure" on the CLI, or put it anywhere in the config file, as it gets uploaded to version control.

Fortunately, there is a "system environment variables" section on the CircleCI website, that allows you to upload system variables such as the AWS private and public key of the IAM user. As we are only using S3 through CircleCI, we don't have to worry about the location (e.g. us-west-2).

Without doing the setup on the CircleCI dashboard though, this code wouldn't be working, because there seems to be no link to an IAM user with permissions to access this bucket.
```
      - run:
         command: sudo pip install awscli
      - run:
         command: |
           cd ~/blogtozip/beats
           aws s3 cp $CIRCLE_SHA1.tar.gz s3://csuneat-project-2/Uploads/
```
Note how at the end we use another environment variable to get the SHA1 of the commit that is being ran.


##### Next Steps
On Friday, we are going to have a group meeting to discuss what work will be required over the weekend to get the project completed on time. I believe me and Shahid will be working on AWS, everyone else will be working on HashiCorp, then we will all work on getting the websites and Datadog deployed to the servers next week.
