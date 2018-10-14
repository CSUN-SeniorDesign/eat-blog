+++ title = "Shahid's Blog. Week 1" date = "2018-10-14" +++
## Shahid's Blog. Week 1
#### What's new this week?

##### Setting up a docker container that hosts a website through apache PART 1
##### Setting up a dockerfile
A dockerfile will create an image that will then be transformed from a blueprint into a container. In other words a dockerfile is a blueprint for a blueprint. Something important to note is that there can be multiple layers of blueprints stacked on each other like with the process of designing architecture.

1. First make a directory and name it something descriptive:
  ```
  mkdir ~/fa480.club-base
  ```

  This directory will act as the base "blueprint" for our other "blueprints" to build on.
  Essentially this directory will store a dockerfile that will create an image when built. Then another directory's stored dockerfile will create another image using the first image as a base.

2. Change directory into the newly created folder or just use your favorite editor to create a file and make sure it's called "Dockerfile"
  ```
  atom ~/fa480.club-base/Dockerfile
  ```

3. Next we need to give some steps the "builder" should follow in order to make our image.
  ```
  FROM ubuntu:14.04.5
  ```
  We are telling the builder we want to use Ubuntu 14.04.5 as a base linux image for all our other images to be build from.

4. We want to run linux commands on our linux image and in order to do so we have Docker's ```RUN``` command:
  ```
  RUN echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections
  ```
  We are telling the linux machine that we are running in an environment where user input cannot be given so don't ask or wait for any.

5. We should probably write some comments on what our commands are doing as well as the next set of commands:
  ```
  # Installing minimum software to get the website running.
  RUN apt-get update
  RUN apt-get install -y apache2
  RUN apt-get install -y curl
  RUN apt-get install -y dpkg
  RUN apt-get install -y git
  RUN apt-get install -y python-pip
  RUN apt-get install -y wget
  RUN update-rc.d -f apache2 remove && update-rc.d -f apache2 defaults
  ```

  Comments always start with ```#```
  Here we are downloading and installing the minimum amount of software in order to get our webserver running.

6. Save your file and make sure you are within the directory that holds the Dockerfile then run the command that will create the image:
  ```
  docker build --rm=true -t fa480.club-base .
  ```

  The ```--rm=true``` will remove other images that will be created with each ```RUN``` command.
  The ```-t``` is a way to give the new image a name.
  And finally the ```.``` is a way of saying "the current directory"

Now if you run the command ```docker images``` you should see your newly created image.

Tune in next week for PART 2 where I'll explain how to set up a static site with hugo.
