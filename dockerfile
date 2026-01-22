#use an official python runtime as a parent image
FROM python:3.13-slim

# set the working directory in the container
WORKDIR /Calculator

#Copy the current directory content into the container at /app
COPY . /Calculator

#Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r Requirements.txt

#Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV FLASK_APP=Calculator.py

#Run the flask app
#CMD ["python", "Calculator.py"]
CMD ["flask", "run", "--host=0.0.0.0"]