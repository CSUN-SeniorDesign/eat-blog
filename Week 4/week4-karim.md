## Shahid's Blog. Week 4
#### What's new this week?

##### Learning about Ansible
Much like a bash script allows a user to run several commands at once, Ansible allows an administrator to apply several changes to a server or group of servers at once. This is done with a list of commands that's consolidated into a yml file called a playbook.

##### Bash Script vs Ansible Playbook
Here is a simple bash script: <br>

```
apt-get install apache2
apt-get install git
```

Wow the Bash Script looks really short right? <br>
Let's now take a look at the Ansible Playbook: <br>
```
    ---
    - hosts: apache
      sudo: yes
          tasks:
            - name: install apache2 and git packages
              apt: name= {{ item }} update_cache=yes state=latest
              with_items:
                - apache2
                - git
```
Even though the Bash Script is much shorter, the Ansible playbook forces you to document what you're doing. Not only that, the playbook can be used on many different machines automatically while the bash script would have to be run one by one on each machine. But if you like Bash Scripts, don't get encouraged because they're still really useful! (Like in the next section...)

##### Installing Ansible
Ansible can be installed in 4 easy steps:
  1. Add a repository manager:

  ```
  sudo apt-get -y install software-properties-common
  ```

  2. Add the ansbile repository:

  ```
  sudo apt-add-repository ppa:ansible/Ansible
  ```

  3. Update the available packages:

  ```
  sudo apt-get -y update
  ```

  4. Install ansible:

  ```
  sudo apt-get -y install ansible
  ```

That's all it takes to install Ansible!

##### Configuring Ansible
Ansible can be configured in 3 easy steps:
  1. Create an SSH Key:

  ```
  ssh-keygen
  ```

  2. Share SSH key with all remote hosts to be used with ansible:

  ```
      yes '' | ssh-copy-id username@remote_host
  ```

    A bash script can be used to give ssh keys to multiple servers at once
    ```
        #!/bin/bash
        for ip in `cat /home/list_of_servers`; do
        ssh-copy-id -i ~/.ssh/id_rsa.pub $ip
    ```

    Replace '/home/list_of_servers' with the location of a file that contains the IP addresses of the servers. Also replace '~/.ssh/id_rsa.pub' with the location of the ssh key you want to use on those servers listed in the list_of_servers file.

  3. Configure Ansible hosts file:
    ```
    sudo nano /etc/ansible/hosts
    ```
      Inside the hosts file type this:
      ```
      [group_name]
      alias ansible_ssh_host=your_server_id
      ```
      3a. Then configure the group file named apache:
        ```
        sudo mkdir /etc/ansible/group_vars
        sudo nano /etc/ansible/group_vars/apache
        ```

      Inside the apache file type this:
      ```
      ---
      ansible_ssh_host: root
      ```
Congratulations! You've set up Ansible!
