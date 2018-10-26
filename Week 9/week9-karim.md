+++
title = "Shahid's Blog. Week 9."
description = "Project 4"
tags = [
    "Blog", "beats", "Shahid", "CIT 480",
]
date = "2018-10-25"
categories = [
    "Blog",
]
menu = "main"
+++

#### What's new this week?
#### Setting up a file server
This week I spent my time converting an old windows laptop to a ubuntu file server. In order to access my files, I decided to use SCP and in order to do so I would need to set up SSH that's accessible over another network.

## Setting up SSH Login
#### Requirements:
1. A client
2. A server
3. A router with admin access

##### On Server:
1. Install SSH and IPtables software
```
sudo apt install -y openssh-server iptables-persistent
```

2. Set up SSH on a port other than 22 and > 1024.

    2a. Open up the file
    ```
    sudo nano /etc/ssh/ssh_config
    ```

    2b. Find the line
    ```
    # Port 22
    ```

    2c. Change the line to the desired port number.

    2d. Restart the sshd service.
    ```
    service sshd restart
    ```

3. Set up iptables to allow incoming connections

    3a. Flush the iptables using the command:
    ```
    sudo iptables -F
    ```

    3b. Add firewall rules.
    ```
    sudo iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
    ```

    3c. Accept SSH/HTTP/HTTPS connections.
    ```
    sudo iptables -A INPUT -i lo -j ACCEPT

    sudo iptables -A OUTPUT -o lo -j ACCEPT

    sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT

    sudo iptables -A INPUT -p tcp --dport 80 -j ACCEPT

    sudo iptables -A INPUT -p tcp --dport 443 -j ACCEPT
    ```

    3d. Drop all other connections.
    ```
    sudo iptables -P INPUT DROP
    ```

    3e. Save the iptables rules and reload them.
    ```
    sudo netfilter-persistent save
    sudo netfilter-persistent reload
    ```

##### On Client:
1. Run this command:
```
ssh-keygen -t rsa -N "" -f /home/$USER/.ssh/id_rsa
```

2. Run this command:
```
ssh-copy-id -i /home/$USER/.ssh/id_rsa shahid@111.111.111.111 -p 22
```
3. Enter password.

4. Login using the public key (This should not ask you for a password login)
using this command:
```
  ssh -i /home/$USER/.ssh/id_rsa.pub shahid@111.111.111.111 -p 22

  ssh -p 22 shahid@111.111.111.111
```

5. SCP file copying:
```
scp -P 22 -r ~/Desktop/shahid-karim-blog shahid@111.111.111.111:~/Desktop/
```

##### On Router:
1. Login to the router's interface using the server machine.
2. Go to port forwarding.
3. Create a new port forward rule.
4. Give it a name.
5. Pick a unused port # > 1024.
6. Save the new port forward rule.
7. (Optional) While logged in, create rules for port forwarding for http and https.
