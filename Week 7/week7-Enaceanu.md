## Alex's Blog. Week 7

#### Project 3
Project 3 is similar to the previous one, except we will be using different
technologies. Instead of Packer, we will be using Docker. We will also be using
containers (via Docker).

#### Setup Docker on local machine
These instructions will be for Ubuntu.

Update the apt package index:

    $ sudo apt-get update

Install packages to allow apt to use a repository over HTTPS:

    $ sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    Software-properties-common
 Add Docker’s official GPG key:

    $ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add

Verify key with fingerprint:

    $ sudo apt-key fingerprint 0EBFCD88

Should return:

    pub   4096R/0EBFCD88 2017-02-22
          Key fingerprint = 9DC8 5822 9FC7 DD38 854A  E2D8 8D81 803C 0EBF CD88
    uid                  Docker Release (CE deb) <docker@docker.com>
    sub   4096R/F273FCD8 2017-02-22

Run command to setup stable repo:

    $ sudo add-apt-repository \
     "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
    $(lsb_release -cs) \stable"`

Actual install:

    $ sudo apt-get update

Install the latest version of Docker CE

    $ sudo apt-get install docker-ce

Verify that Docker CE is installed correctly by running the hello-world image:

    $ sudo docker run hello-world

You should see: Hello from Docker! And a description of the steps the program
ran to generate the message.

Install PIP:

    $ sudo apt-get install python-pip

Verify pip install with:

    pip --version

Create an empty directory (I called it Docker_dir):

    MKDIR <directory name>

CD into that dir

Create 3 files inside this directory: Dockerfile, app.py, requirements.txt

Create Dockerfile:

  $  touch Dockerfile app.py requirements.txt

Add necessary permissions:

    Chmod 0755 Dockerfile app.py requirements.txt

Dockerfile contents:

Use an official Python runtime as a parent image

    FROM python:2.7-slim

Set the working directory to /app

    WORKDIR /app

Copy the current directory contents into the container at:

    /app COPY . /app

Install any needed packages specified in requirements.txt

    RUN pip install --trusted-host pypi.python.org -r requirements.txt

Make port 80 available to the world outside this container

    EXPOSE 80

Define environment variable

    ENV NAME World

Run app.py when the container launches
CMD ["python", "app.py"]

requirements.txt contents:
    Flask
    Redis

App.py contents:

    from flask import Flask
    from redis import Redis, RedisError
    import os
    import socket

Connect to Redis
    redis = Redis(host="redis", db=0, socket_connect_timeout=2, socket_timeout=2)

    app = Flask(__name__)

    @app.route("/")
    def hello():
        try:
            visits = redis.incr("counter")
        except RedisError:
            visits = "<i>cannot connect to Redis, counter disabled</i>"

        html = "<h3>Hello {name}!</h3>" \
               "<b>Hostname:</b> {hostname}<br/>" \
               "<b>Visits:</b> {visits}"
        return html.format(name=os.getenv("NAME", "world"), hostname=socket.gethostname(), visits=visits)

    if __name__ == "__main__":
        app.run(host='0.0.0.0', port=80)

Run command to install redis and flask libraries:

    pip install -r requirements.txt

Build the app:ls command should show the three files we created. Then run:

    $ sudo docker build -t friendlyhello .

An image will build.Run the below command to display the newly built image.

    $ sudo docker image ls

Run the app:

    $ sudo docker run -p 4000:80 friendlyhello

You should see a message that Python is serving your app at http://0.0.0.0:80. But that message is coming from inside the container, which doesn’t know you mapped port 80 of that container to 4000, making the correct URL http://localhost:4000.
Go to that URL in a web browser to see the display content served up on a web page:

    Hello world!
    Hostname: 73fde6e646bf
    Visits: Cannot connect to Redis, counter disabled

(redis warning ok for now)

You can also use the curl command in a shell to view the same content:

    $ curl http://localhost:4000

#### Share your image

Log in with docker ID:

    $ sudo docker login

#### Tag the image

docker tag image username/repository:tag

My test example is:

    $ docker tag image ae637/testrepo:test

#### Publish the image

    $ docker push username/repository:tag

My example:

    $ docker push ae637/testrepo:test

Once you are finished you can see your results on the Docker Hub
(which is public FYI). You can pull and run the image from the remote
repository. From now on, you can use docker run and run your app on any machine
with this command:

    $ docker run -p 4000:80 username/repository:tag

My Example:

    $ docker run -p 4000:80 ae637/testrepo:test

Now you can pull your image wherever docker runs.
