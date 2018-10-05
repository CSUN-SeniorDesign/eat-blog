# Week 6 blog

###### The rundown this Week

The week ended up being a bit more challenging then what the whole group would have liked partly due to setting up the base ami and packer. As well as making sure that we were able to automate some of the tasks that were required through a cronjob script. I mainly worked with Erik and Alex for the majority of setting up the packer as well as installing the datadog agent and extracting the metrics that we needed. Currently we  ran into a good amount of issues over this past week such as not being able to have access to the s3 bucket when trying to access it even though we had our credentials. We discovered that more then anything we needed to run the base ami so then our IAM permission would be granted access. To bypass this we ended up making the s3 bucket public only for the time that we need to run our scripts, after we are done and launch packer we will go ahead and make it private again.

###### Future work to finish project 2

So far we have finished the cronjobs but they just need further testing to make sure that they are reaching our staging site. We ran the python scripts but are currently getting an issue about it not recognizing our staging site which might have to do with how we refernce it. Some of the metrics that we are a well recieving do not seem to be updating correctly or are not displaying currently so I am working with Alex and Erik to try and display the metrics properly most likely what the problem is though that our configuration file that holds the modules is not specified and we as well need to edit the config.yaml file.  


###### Next project ideas

For the next project we have decided to go back to our previous method of assigning roles individually rather than by group. This will allow for more work to be distributed evenly amongst all group members and will allow each person to focus on a handful of things than have a whole group focus on an amount of things, by going back to this way we all have equal work.
