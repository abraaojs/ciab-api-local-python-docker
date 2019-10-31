FROM python:alpine3.7
MAINTAINER Abraao Silva <abraaojs.dev@gmail.com>
COPY . /app
WORKDIR /app

COPY dlib-19.17.zip .
RUN unzip dlib-19.17.zip
WORKDIR dlib-19.17
CMD python ./app.py

WORKDIR ..

# Install dependencies:
#COPY requirements.txt .
RUN pip install -r requirements.txt

# Run the application:
ADD app .
CMD ["python", "app.py"]

EXPOSE 5000
