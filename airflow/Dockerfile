# Use the official Apache Airflow image with a specific version
# FROM apache/airflow:2.9.2
FROM apache/airflow:2.9.2-python3.10

# Set the environment variables
# ENV AIRFLOW_HOME=/opt/airflow

# Switch to root user to install dependencies
USER root
# Install OpenJDK-17
RUN apt update && \
    apt-get install -y openjdk-17-jdk && \
    apt-get install -y ant && \
    apt-get clean;

# Set JAVA_HOME
ENV JAVA_HOME /usr/lib/jvm/java-17-openjdk-amd64/
RUN export JAVA_HOME

USER airflow

# Copy requirements.txt into the container
COPY requirements.txt /tmp/

# Install Python dependencies
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Verify installation
# RUN pip show apache-airflow
