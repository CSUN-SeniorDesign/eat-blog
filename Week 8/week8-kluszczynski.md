+++ title = "Tyler's Blog. Week 8." description = "Finishing Lambda" tags = [ "Blog", "beats", "Tyler", "CIT 480", ] date = "2018-10-18" categories = [ "Blog", ] menu = "main" +++

## Tyler's Blog. Week 8.
#### What's new this week?

##### Finishing Project 3
This was the last week for the "last" project. Most of the project is done except for the following: ALB needs to be setup to have 2 separate target groups (one for staging, one for production). This has to be linked to the respective ECS service. This week, I finished the lambda, and would like to discuss the lambda code itself.

##### AWS Lambda
Lambda is a service offered by AWS that allows you to run code snippets without the requirement of a server. These code snippets run based on various triggers. These triggers can be set up using Lambda, and also require IAM permissions. For this project, I used Lambda to automate deployment of AWS ECR images into ECS. Overall, the lambda portion of this assignment took about a week and a half.

##### Lambda - Code Review
The fist step in the process of automating deployment, is creating the lambda handler. Then, the next task is assigning permissions to an AWS Lambda handler. These are both done through terraform, and is covered in last week's blog post. Once your lambda handler/function is setup, then we can start writing the function.

I wrote my function using Python using boto3, but there are numerous options offered by AWS. First, the function fetches an object from s3, which contains the commit SHA of the ECR image to deploy. Staging and production both use exactly the same code.


```
	def my_handler(event, context):
    	bucket = event.get("Records")[0].get("s3").get("bucket")
    	bucket_arn = bucket.get("arn")
    	bucket_name = bucket.get("name")

    	the_object = event.get("Records")[0].get("s3").get("object")
    	filename = the_object.get("key")

    	tag = getFile(bucket_name,filename,filename)
    	containername = ""

    	if filename == "ProductionSite.txt":
        	containername = "beats-production"
    	elif filename=="StagingSite.txt":
        	containername = "beats-staging"

    	print(tag)

    	update(tag,containername,tag)
```

The getFile function in the code above retrieves the tag of the SHA.

```
	def getFile(bucket, filename, filepath):
    	filepath = "/tmp/"+filepath

    	s3client = boto3.client('s3')
    	s3client.download_file(bucket, filename, filepath)

    	txt_file = open(filepath, "r")
    	tag = txt_file.readline()
    	txt_file.close()

    	return tag
```

This tag is used in the update function, along with another parameter based on the site we're updating. The following code sets up the image name, that references the ECR image.

```
	imagename = "507963158957.dkr.ecr.us-west-2.amazonaws.com/beats_repo:"+imagename
	imagename = imagename.rstrip()
```

 After this, we set up container definitions. This is done because it was much simpler to set up the ports using lambda rather than terraform, and it has to set up the image anyway.

```
containerDefinitions=[
            {
          taskDefinitionRev = response['taskDefinition']['family'] + ':' + str(response['taskDefinition']['revision'])
#print taskDefinition
    response = client.update_service(
        cluster='beats-cluster',
        service=containername,
        desiredCount=1,
        taskDefinition=taskDefinitionRev,
        deploymentConfiguration={
            'maximumPercent': 100,
            'minimumHealthyPercent': 40
        }
    )
    #pprint.pprint(response)
print("service updated")
          'name': containername,
                'image': imagename,
                'memory': 300,
                'portMappings': [
                    {
                        'containerPort': 80,
                        'hostPort': 80,
                        'protocol': 'tcp'
                    },
                    {
                        'containerPort': 443,
                        'hostPort': 443,
                        'protocol': 'tcp'
                    }
                ],
                'essential': True,
            },
        ],
```

Finally, we update the service in our cluster with the new task definition we created, along with some deployment configuration.

```
taskDefinitionRev = response['taskDefinition']['family'] + ':' + str(response['taskDefinition']['revision'])
#print taskDefinition
response = client.update_service(
    cluster='beats-cluster',
    service=containername,
    desiredCount=1,
    taskDefinition=taskDefinitionRev,
    deploymentConfiguration={
        'maximumPercent': 100,
        'minimumHealthyPercent': 40
    }
)
#pprint.pprint(response)
print("service updated")
```

At this point, the lambda is completed and should be tested. The most difficult part of lambda was determining how exactly to set up the task definition and deployment update_service. We also had to determine what should be setup using terraform, and what should be setup using the lambda function, which isn't exactly obvious.
