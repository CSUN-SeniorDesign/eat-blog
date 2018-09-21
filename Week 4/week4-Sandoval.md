## Week 4 Blog

#### The rundown this Week

##### Tasks completed

This week I ran into a bit of issues in configuring the s3 bucket initially I had setup my terraform code in the correct format. The first part of my issue is that I did not realize that I needed a back end snippet that would allow me to sync up the current .tfstate file. I needed to include a back end portion which would remotely sync the .tfstate file so that all the changes that we made would be able to add those records to the state file. The second error that I encountered myself with is that I kept getting an error when running the terraform apply command. The issue was that it kept telling me that I needed to add 37 records to the state file. I figured the problem to this was that everyone in my group had been running their terraform scripts for their parts so the state file kept looking for the added changes to add but since I was missing the back end part the state file was not being updated. In order to solve this issue I had to destroy the infrastructure and so did the rest of my teammates just to make sure that no records to add would show up. after doing this I ended up merging the new set of scripts we had to our github repo. when we ran terraform apply within the new updated directory folder all the issues that had arised went away and the state file on the bucket was being updated remotly and without any issues.

##### Future plans

Right now I am helping Shahid with the ansible portion of the project. So far we have the list of commands that will allow us to ssh and configure a web server onto our private servers we just need to figure out coming up with the right syntax to be able to code the commands. After we will be focusing on the second playbook which will allow us to display our blog's web pages.
