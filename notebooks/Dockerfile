FROM jupyter/pyspark-notebook:lab-3.3.4

USER root

# Backup Spark cũ
RUN mv /usr/local/spark /usr/local/spark-old

# Download Spark 3.3.4 using wget
RUN wget https://archive.apache.org/dist/spark/spark-3.3.4/spark-3.3.4-bin-hadoop3.tgz \
    && tar xzf spark-3.3.4-bin-hadoop3.tgz \
    && mv spark-3.3.4-bin-hadoop3 /usr/local/spark-3.3.4-bin-hadoop3 \
    && ln -s /usr/local/spark-3.3.4-bin-hadoop3 /usr/local/spark \
    && rm spark-3.3.4-bin-hadoop3.tgz

# Update SPARK_HOME
ENV SPARK_HOME=/usr/local/spark
ENV PATH=$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin
ENV PYTHONPATH=$SPARK_HOME/python:$SPARK_HOME/python/lib/py4j-0.10.9.5-src.zip:$PYTHONPATH

# Copy JARs from local (except AWS SDK bundle which will be downloaded)
COPY jars/*.jar /usr/local/spark/jars/

# Download AWS SDK bundle inside container (full 268MB version)
RUN cd /usr/local/spark/jars && \
    rm -f aws-java-sdk-bundle*.jar && \
    wget -q https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/1.12.262/aws-java-sdk-bundle-1.12.262.jar

# Upgrade pyspark to match Spark version
RUN pip install --no-cache-dir --upgrade pyspark==3.3.4 python-dotenv

# Fix permissions
RUN fix-permissions /usr/local/spark && \
    fix-permissions /home/$NB_USER

USER $NB_UID

WORKDIR /home/$NB_USER/work