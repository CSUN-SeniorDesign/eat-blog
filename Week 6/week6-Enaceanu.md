## Alex's Blog. Week 6

#### Project 2 continues . . .
For the continuation of project 2 I maintained my focus on Datadog. In the last
blog I talked about how to create an IAM role for Datadog, an important step for
security. I also talked about how to apply the least privileged model via a JSON
script. Since that is all good and done, we can continue to configuring Datadog
on our instances so that we may customize metrics we wish to capture for
our dashboards.

There are many options when it comes to metrics, some of them are already setup
and easy to place on a dashboard such as CPU and memory usage. In this example
we will focus on SSH_checks, but essentially most metrics can be configured the
same way, by configuring the conf.yaml file found in each of the nearly 100
directories that live in the Datadog Agent package conf.d/ folder .
First you must determine where these directories reside on your instance. this
will be slightly different depending on the operating system you are running.
For our NAT instance, we are running Amazon Linux, and the directory can be
found at: /etc/datadog-agent/conf.d/. Once you are in this directory you select the subfolder for the service you want to configure. For us it will be
ssh_check.d. First there will be a example file for you to copy and customize
called conf.yaml.example. I used the VI editor to open the file and change the
parameters to match our desired output. You must also remove the example at the end of the filename.

This can be done with the following command:

      mv conf.yaml.example conf.yaml

Below is the conf.yaml.example file with no changes made:

      init_config:

      instances:
      - host: <SOME_REMOTE_HOST>  # required
      username: <SOME_USERNAME> # required
      password: <SOME_PASSWORD> # or use private_key_file
      private_key_file: <PATH_TO_PRIVATE_KEY>
      private_key_type:         # rsa or ecdsa; default is rsa
      port: 22                  # default is port 22
      sftp_check: False         # set False to disable SFTP check; default is True
      add_missing_keys: True    # default is False

As you can see, Datadog makes configuration  very easy with commented out notes that tell you what parameters are required at a minimum for the metric collection to work.For SSH checks you need to specify an instance ID: which can be pulled from your AWS environment, and a user name: EC2-user. If you don't use a password, you will need to specify the path to you private key. Those are the only 3 parameters you need to specify to get it going! The rest of the options will default to what is listed above, i.e. port 22 since we are talking SSH and key type, etc.

#### Once your conf.yaml file is altered . . .

You must stop Datadog Agent and then restart it. Once again this will be different dependent on your operating system. For Linux use the below commands.

This can be done with the following commands:

      sudo stop datadog-agent

You will get confirmation the service is stopped, then start it with:

      sudo start datadog-agent

You will get confirmation the service has started. Now you must check the status of your agent to ensure that the specific check you just configured is working with this command (once again OS specific) fort Linux:

      sudo datadog-agent status

It will show up under the checks section labeled with the check in question. Here is an example:


      Running Checks
      ==============

        ssh_check (1.3.1)
        -----------------
             Instance ID: ssh_check:5763bcd0062a6f5b [OK]
             Total Runs: 65
             Metric Samples: 0, Total: 0
             Events: 0, Total: 0
             Service Checks: 2, Total: 130
             Average Execution Time : 20ms

You can the configure your dashboard to visualize your metric!!
