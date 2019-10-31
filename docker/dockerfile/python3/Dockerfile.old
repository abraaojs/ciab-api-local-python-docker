FROM centos:7
RUN yum update -y && \
yum install -y epel-release && \
yum install -y python36 python36-pip python36-devel mysql-devel unzip && \
yum install -y gcc g++ gcc-c++ cmake make

RUN mkdir /app
WORKDIR /app

COPY dlib-19.17.zip .
RUN unzip dlib-19.17.zip
WORKDIR dlib-19.17
RUN python36 setup.py install 

WORKDIR ..

# Install dependencies:
COPY requirements.txt .
RUN pip3.6 install -r requirements.txt

# Run the application:
ADD app .
CMD ["python36", "app.py"]
