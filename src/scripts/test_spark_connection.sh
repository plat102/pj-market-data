# scripts/test_spark_connection.sh
#!/bin/bash
echo "Testing Spark Master UI port (8080)..."
nc -zv spark-master 8080

echo "Testing Spark Master submission port (7077)..."
nc -zv spark-master 7077
