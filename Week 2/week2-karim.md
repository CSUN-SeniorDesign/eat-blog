+++ title = "Shahid's Blog. Week 2" date = "2018-10-14" +++
## Shahid's Blog. Week 2
#### What's new this week?

##### Setting up a docker container that hosts a website through apache PART 2
##### Setting up ANOTHER dockerfile
So last week we made a dockerfile that created our "base" image that handled downloading and installing all the software we'd need for this part.

1. As with the first part, make a directory and name it something descriptive:
  ```
  mkdir ~/production-site
  ```

  We have to create a new directory since the file has to be called "Dockerfile" and we can't have two of the same files in the same directory.

2. Change directory into the newly created folder or just use your favorite editor to create a file and make sure it's called "Dockerfile"
  ```
  atom ~/production-site/Dockerfile
  ```

3. Next we need to give some steps the "builder" should follow in order to make our image.
  ```
  FROM fa480.club-base
  ```

  Please note that unlike last time we are not using Ubuntu:14.04.5 in our ```FROM``` command.
  This is because we have already created a new image we want to use as our base. Make no mistake, the fa480.club-base image we made IS Ubuntu 14.04.5 but we've gone ahead and changed only the software installed on it.  

4. Now the first thing we want to do after telling the builder what our base image is installing hugo (our static site generator):
  ```
  # Installing Hugo
    RUN wget https://github.com/gohugoio/hugo/releases/download/v0.49/hugo_0.49_Linux-64bit.deb
    RUN dpkg -i hugo_0.49_Linux-64bit.deb
    RUN pip install awscli --upgrade --user
  ```

  Don't forget to add comments to each logical chunk of code to remember what it does.
  We are downloading the deb package that holds hugo, then using our package manager to install hugo. Finally we're including awscli for giggles.

5. Since you might not have content lying around, I've gone to the trouble of adding some for you:
  ```
  # Get the website from github
  RUN git clone https://github.com/CSUN-SeniorDesign/eat-blog.git
  ```

  This will grab my blog files from my github and put it on the home directory of the image to be built.

6. Next we have to do some file moving and rearranging in order to get our site working well and looking good:
  ```
  # Pre hugo configuration
  RUN hugo new site beats
  RUN mv /eat-blog/arabica /beats/themes/arabica
  RUN rm -rf /beats/themes/arabica/exampleSite/*
  RUN mv /eat-blog/config.toml /beats/config.toml
  RUN mkdir /beats/content/post/
  RUN mv /eat-blog/* /beats/content/post/
  ```
  This creates a new site directory, where we'll need to move our theme and get rid of any site data we get from the theme. Then we'll have to update our configuration file to tell hugo that we are using a non default theme. Finally we move our blog files into the directory that hugo will be looking for them.

7. Afterwards we have to clean up some more and actually run hugo so that our site will be created:
  ```
  # Pre hugo clean up
  RUN rm /beats/content/post/BEATS-Uploader.py
  RUN rm /beats/content/post/ProductionSite.txt
  RUN rm /beats/content/post/S3-Fetch.py

  # Use hugo to create the website
  RUN cd /beats && hugo
  ```
8. Now that we have our site built, we need to actually host it using apache2
  ```
  # Move the website to /var/www/html
  RUN mv /beats/public/* /var/www/html
  EXPOSE 80/tcp
  EXPOSE 443/tcp
  ```
9. Then we have to tell our builder that when our image is run, that the apache2 service should start when the image is started.
  ```
  CMD service apache2 start && tail -f /dev/null
  ```

  The ```tail -f /dev/null``` just ensures that our new docker container will stay running even in the background.

10. Finally we have to run the command that builds our image from the dockerfile in this directory:
  ```
  docker build --rm=true -t production-site .
  ```

  Again please note:
  The ```--rm=true``` will remove other images that will be created with each ```RUN``` command.
  The ```-t``` is a way to give the new image a name.
  And finally the ```.``` is a way of saying "the current directory"

  Now if you run the command ```docker images``` you should see your newly created image.

##### Turning images into containers
```docker run -dit production-site```

This command will create a container from the image "production-site"
```-d``` makes sure that it runs in the background
```-i``` makes sure that the STDIN is always open
```-t``` makes sure that you can login to the container

Running the above command will give you an imageid.
If you want to login to the container with that imageid:

```docker exec -it [imageid] /bin/bash```
