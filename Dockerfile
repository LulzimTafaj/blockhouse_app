# Use an official Python runtime as a parent image
FROM python:3.10.12

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Copy requirements.txt into the container
COPY requirements.txt /app/

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the rest of the project, excluding images and reports directories
COPY . /app/
RUN rm -rf /app/images /app/reports  # Exclude unnecessary directories

# Expose port 8000 (to match docker-compose)
EXPOSE 8000

# Use Gunicorn to serve the Django app in production
CMD ["gunicorn", "blockhouse.wsgi:application", "--bind", "0.0.0.0:8000"]

# Optional Healthcheck
HEALTHCHECK CMD curl --fail http://localhost:8000/ || exit 1
