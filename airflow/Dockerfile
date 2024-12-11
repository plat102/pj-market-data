# Use the official Apache Airflow image with a specific version
# FROM apache/airflow:2.9.2
FROM apache/airflow:2.9.2-python3.10

# Set the environment variables
# ENV AIRFLOW_HOME=/opt/airflow

# Switch to root user to install dependencies
# USER root

USER airflow

# Copy requirements.txt into the container
COPY requirements.txt /tmp/

# Install Python dependencies
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Verify installation
# RUN pip show apache-airflow
