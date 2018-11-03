+++
title = "Shahid's Blog. Week 10."
description = "Multiple sites on apache"
tags = [
    "Blog",
    "beats",
    "Shahid",
    "COMP 480",
    "Project 5",
]
date = "2018-11-02"
categories = [
    "Blog",
]
+++

## Setting up Multiple Sites on Apache

1. Set up folders for each site:
```
  sudo mkdir -p /var/www/shahid-karim-blog.com/public_html

  sudo mkdir -p /var/www/skarim3000.com/public_html
```

2. Change the directory ownership to the user from root:
```
  sudo chown -R $USER:$USER /var/www/shahid-karim-blog.com/public_html

  sudo chown -R $USER:$USER /var/www/skarim3000.com/public_html

  sudo chmod -R 755 /var/www
```

3. Create virtual hosts configuration files
```
  sudo cp /etc/apache2/sites-available/000-default.conf /etc/apache2/sites-available/shahid-karim-blog.com.conf

  sudo cp /etc/apache2/sites-available/000-default.conf /etc/apache2/sites-available/skarim3000.com.conf
```

4. Add this to the above conf files:
```
  sudo nano /etc/apache2/sites-available/shahid-karim-blog.com.conf

  <VirtualHost *:80>
    ServerAdmin admin@test.com
    ServerName shahid-karim-blog.com
    ServerAlias www.shahid-karim-blog.com
    DocumentRoot /var/www/shahid-karim-blog.com/public_html
    ErrorLog ${APACHE_LOG_DIR}/error.log
    CustomLog ${APACHE_LOG_DIR}/access.log combined
  </VirtualHost>

  sudo nano /etc/apache2/sites-available/skarim3000.com.conf

  <VirtualHost *:80>
      ServerAdmin admin@example.com
      ServerName skarim3000.com
      ServerAlias www.skarim3000.com
      DocumentRoot /var/www/skarim3000.com/public_html
      ErrorLog ${APACHE_LOG_DIR}/error.log
      CustomLog ${APACHE_LOG_DIR}/access.log combined
  </VirtualHost>
```

5. Enable the virutal hosts using a2ensite
```
  sudo a2ensite shahid-karim-blog.com.conf
  sudo a2ensite skarim3000.com.conf
```

6. Restart the apache2 service.
```
  sudo service apache2 restart
```

7. Add the IP address of the server to the hosts file of any client that wants to visit the site if the domain isn't owned.
```
  ipaddress example.com
  same ipaddress test.com

  ex:
  192.168.0.5 example.com
  192.168.0.5 test.com

  111.111.111.111 www.skarim3000.com # file server
  111.111.111.111 www.shahid-karim-blog.com # blog site
```

8. If you don't want to deal with hosts file, leave this html file in your /var/www/html folder:

  Note: You have to move your sitename.com directory into the /var/www/html folder. This will internally direct the user of the site without them having to remember the long site names.

```
<html>
	<body>
		Welcome to html root. The two sites hosted here are:

		<a href="shahid-karim-blog.com/public_html/index.html">www.shahid-karim-blog.com</a> and
		<a href="skarim3000.com/public_html/index.html">www.skarim3000.com</a>
	<body>
<html>
```
