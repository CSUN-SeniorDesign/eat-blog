## Erik's Blog. Week 5
#### What's new this week?
##### How to create a dashboard with metrics using Datadog
The Datadog Agent allows you to collect metrics from your instances and a dashboards can be a very useful tool to monitoring those metrics from your instances.
![Image of Datadog](https://datadog-prod.imgix.net/img/datadog_logo_share_tt.png)

###### 1. Install the Datadog Agent
We need to install the Datadog Agent on our target hosts so that we can collect the metrics from our hosts. The ideal solution is to do this with Ansible but I will demonstrate how to install it on an Ubuntu machine.
  1. Login to your Datadog account (https://www.datadoghq.com/) and select `Integrations` at the top of the page and then click `Agent`
  2. Select which OS you want to install the Agent on, copy the one-step installation code from Step 1 (Should look similar to the code below) and SSH into your host and paste the code.
`DD_API_KEY=9289c8******** bash -c "$(curl -L https://raw.githubusercontent.com/DataDog/datadog-agent/master/cmd/agent/install_script.sh)"`
  3. You should now be able to click on `Infrastructure` and then `Infrastructure List` to see a list of hosts where you have installed the agent on.

###### 2. AWS Integration
Next step is to sync our AWS account to Datadog so what we can get an overlook of our full infrastructure.
 1. Click on `Integrations` from the menu on the top and select `Integrations`.
 2. Search for AWS in the search field and select it.
 3. You'll be taken to a page that asks for your AWS account ID and AWS Role name.
Enter the AWS ID of your organization (if you are in one, 507963158957 in our case).
Enter `DatadogAWSIntegrationRole` for the AWS Role name.
 4. Click on `Install/Update configuration` in the left corner.
 5. DONE! Click on `Infrastructure` and then `Infrastructure List` again and you should now be able to see your full infrastructure.

###### 3. Screenboard vs Timeboard
* **Screenboards** are used for status boards and sharing data. All graphs in a screenboard can have individual time scopes and they are used to monitor the overall health over your infrastructure.
* **Timeboards** are used for troubleshooting and correlation. The graphs used share the same time scopes. Once you have identified something of a concern on a screenboard you use the timeboard to troubleshoot that particular concern.


1. I am using a Timeboard for this example and you can create one by clicking `Dashboards` select `New Dashboard` and then `New Timeboard`.
2. I will go over how to create a graph for CPU usage. Drag and Drop the `Timeseries` onto your dashboard and a new window will popup.
3. Click on `system.load.1` and type `system.cpu.idle`
4. Click `Graph Metric` to add a new field and add `system.cpu.system`.
5. Repeat step 4. for the metrics: `system.cpu.iowait`,`system.cpu.user`,`system.cpu.stolen` and `system.cpu.guest`.
6. Give your graph a suitable title and then press `Save` and you are done.
