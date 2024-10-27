# FROM docker.io/bitnami/spark:3.5.3

# USER root

# # Install prerequisites
# RUN apt-get update && apt-get install -y curl

# RUN curl -O https://repo1.maven.org/maven2/software/amazon/awssdk/s3/2.18.41/s3-2.18.41.jar \
# && curl -O https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk/1.12.367/aws-java-sdk-1.12.367.jar \
# && curl -O https://repo1.maven.org/maven2/io/delta/delta-core_2.12/2.2.0/delta-core_2.12-2.2.0.jar \
# && curl -O https://repo1.maven.org/maven2/io/delta/delta-storage/2.2.0/delta-storage-2.2.0.jar \
# && mv s3-2.18.41.jar /opt/bitnami/spark/jars \
# && mv aws-java-sdk-1.12.367.jar /opt/bitnami/spark/jars \
# && mv delta-core_2.12-2.2.0.jar /opt/bitnami/spark/jars \
# && mv delta-storage-2.2.0.jar /opt/bitnami/spark/jars
# Use the official Spark image as the base
FROM bitnami/spark:3.5.3

# Set environment variables for Spark
ENV SPARK_HOME=/opt/bitnami/spark \
    PATH=$PATH:/opt/bitnami/spark/bin \
    SPARK_MODE=master \
    SPARK_RPC_AUTHENTICATION_ENABLED=no \
    SPARK_RPC_ENCRYPTION_ENABLED=no \
    SPARK_LOCAL_STORAGE_ENCRYPTION_ENABLED=no \
    SPARK_SSL_ENABLED=no

# Copy custom configuration files (optional)
COPY spark-defaults.conf $SPARK_HOME/conf/spark-defaults.conf

# Expose ports used by the Spark master
EXPOSE 7077 8080

# Command to run Spark master service
ENTRYPOINT ["/opt/bitnami/scripts/spark/entrypoint.sh"]
CMD ["spark-class", "org.apache.spark.deploy.master.Master", "--host", "0.0.0.0"]
