# 1. Use an official Python runtime as a parent image
FROM python:3.11-slim

# 2. Set the working directory in the container
WORKDIR /app

# 3. Copy the current directory contents into the container at /app
COPY . /app

# 4. Copy the templates directory into the container
COPY templates/ /app/templates/

# 5. Install any required packages specified in requirements.txt
# Make sure you have a requirements.txt in the root of your project
RUN pip install --no-cache-dir -r requirements.txt

# 6. Make port 80 available to the world outside this container
EXPOSE 8080

# 7. Set the default command to run the app
CMD ["python", "app.py"]

