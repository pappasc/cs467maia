# CentOS base image
FROM centos:7

# Install Python 2.7 in container
RUN yum install gcc -y
RUN yum install wget -y
RUN wget https://www.python.org/ftp/python/2.7.10/Python-2.7.10.tgz
RUN tar xzf Python-2.7.10.tgz
WORKDIR Python-2.7.10
RUN ./configure
RUN python2.7 -V

# Install texlive in container
RUN yum install texlive -y 

# Install pip for later install of dependencies
RUN yum install epel-release -y
RUN yum install python-pip -y

# Copy source directory into container
RUN mkdir /interpreter-api
WORKDIR /interpreter-api
COPY interpreter_api .

# Install dependencies of application
RUN pip install -r requirements.txt

# Run Flask application when spinning up docker container
CMD [ "python2.7", "view.py"]

# References: 
# [1] https://hub.docker.com/_/python/							re: installing python from base image
# [2] https://milq.github.io/install-latex-ubuntu-debian/		re: installing latex
# [3] https://docs.docker.com/engine/reference/commandline/run/ re: use of --publish
# [4] https://myopswork.com/install-python-2-7-10-on-centos-rhel-75f90c5239a5 re: steps to install python, used above