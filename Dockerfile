# Use an official Python runtime as a parent image
FROM python:3.11

# Set environment variables for Django
ENV DJANGO_SETTINGS_MODULE=bloggingApp.settings

# Set the working directory in the container
WORKDIR /blogapp

# Copy the requirements file into the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install -r requirements.txt

# Copy the project files into the container
COPY . .

# Expose the port that the Django app will run on (e.g., 8000)
EXPOSE 8000

# Run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
