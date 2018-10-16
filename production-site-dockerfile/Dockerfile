FROM fa480.club-base

# First cd into the folder this docker image is in.
# Then build this dockerfile image by running: docker build --rm=true -t production-site .
# To run this dockerfile: docker run -dit production-site
# To log into the container the above command makes: docker exec -it [imageid] /bin/bash
# The imageid comes from the run command.
# Do not include the [ ] around the imageid.

# Installing Hugo
RUN wget https://github.com/gohugoio/hugo/releases/download/v0.49/hugo_0.49_Linux-64bit.deb && \
dpkg -i hugo_0.49_Linux-64bit.deb && \
rm hugo_0.49_Linux-64bit.deb && \
pip install awscli --upgrade --user

# Get the website from github
RUN git clone https://github.com/CSUN-SeniorDesign/eat-blog.git

# Pre hugo configuration
RUN hugo new site beats && \
mv /eat-blog/arabica /beats/themes/arabica && \
rm -rf /beats/themes/arabica/exampleSite/* && \
mv /eat-blog/config.toml /beats/config.toml && \
mkdir /beats/content/post/ && \
mv /eat-blog/* /beats/content/post/ && \
# Pre hugo clean up
rm /beats/content/post/BEATS-Uploader.py && \
rm /beats/content/post/ProductionSite.txt && \
rm /beats/content/post/S3-Fetch.py && \
rm -rf eat-blog && \
# Use hugo to create the website
cd /beats && hugo && \
# Move the website to /var/www/html
mv /beats/public/* /var/www/html && \
rm -rf beats

EXPOSE 80/tcp
EXPOSE 443/tcp

# Start apache2 service
RUN service apache2 start

# Change apache2's configuration to include 2 headers
RUN a2enmod headers && \
curl icanhazip.com | tee /etc/apache2/serverip && \
echo "export servername=`</etc/hostname`" | tee -a /etc/apache2/envvars && \
echo "export serverip=`</etc/apache2/serverip`" | tee -a /etc/apache2/envvars && \
echo "PassEnv servername" >> /etc/apache2/apache2.conf && \
echo "PassEnv serverip" >> /etc/apache2/apache2.conf && \
echo "Header set X-Hostname %{servername}e" >> /etc/apache2/apache2.conf && \
echo "Header set X-Private-IP %{serverip}e" >> /etc/apache2/apache2.conf

# Move the script from the host to the image that installs datadog.
COPY datadog.sh /home/datadog.sh
RUN chmod 777 /home/datadog.sh

# Link datadog to the image for monitoring.
# RUN ./home/datadog.sh

CMD service apache2 start && tail -f /dev/null
