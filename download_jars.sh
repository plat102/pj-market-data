#!/bin/bash

# Define the target directory
JARS_DIR="./spark/jars"

# Create the directory if it doesn't exist
mkdir -p $JARS_DIR

# Download the JAR files to the specified directory
curl -o $JARS_DIR/s3-2.18.41.jar https://repo1.maven.org/maven2/software/amazon/awssdk/s3/2.18.41/s3-2.18.41.jar
curl -o $JARS_DIR/aws-java-sdk-1.12.367.jar https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk/1.12.367/aws-java-sdk-1.12.367.jar
curl -o $JARS_DIR/delta-core_2.12-2.2.0.jar https://repo1.maven.org/maven2/io/delta/delta-core_2.12/2.2.0/delta-core_2.12-2.2.0.jar
curl -o $JARS_DIR/delta-storage-2.2.0.jar https://repo1.maven.org/maven2/io/delta/delta-storage/2.2.0/delta-storage-2.2.0.jar
curl -o $JARS_DIR/hadoop-aws-3.3.4.jar https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/3.3.4/hadoop-aws-3.3.4.jar
curl -o $JARS_DIR/aws-java-sdk-bundle-1.11.1026.jar https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/1.11.1026/aws-java-sdk-bundle-1.11.1026.jar

echo "JAR files downloaded to $JARS_DIR"
