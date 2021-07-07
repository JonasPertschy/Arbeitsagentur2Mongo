# set base image (host OS)
FROM python:alpine

# set the working directory in the container
WORKDIR /code

# copy requirements first to make it faster
COPY src/requirements.txt .

# install dependencies
RUN pip install -r requirements.txt

# copy the content of the local src directory to the working directory
COPY src/ .

# command to run on container start
CMD [ "python", "./script.py" ]