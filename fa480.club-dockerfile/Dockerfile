FROM ubuntu:14.04.5

# First cd into the folder this docker image is in.
# Then build this dockerfile image by running: docker build --rm=true -t fa480.club-base .
# Tell the image that it's noninteractive so there wont be any waiting for prompts.
RUN echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections

# Installing minimum software to get the website running.
RUN apt-get update && \
apt-get install --no-install-recommends -y apache2 curl dpkg git python-pip wget && \
rm -rf /var/lib/apt/lists/*
