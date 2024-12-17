# spark/jobs/test_connection.py
from pyspark.sql import SparkSession

def main():
    try:
        spark = SparkSession.builder \
            .appName("TestConnection") \
            .master("spark://spark-master:7077") \
            .getOrCreate()
        
        # Create simple test DataFrame
        test_df = spark.createDataFrame([(1, "test")], ["id", "value"])
        count = test_df.count()
        print(f"Successfully connected to Spark! Test DataFrame count: {count}")
        
        spark.stop()
        return True
    except Exception as e:
        print(f"Failed to connect to Spark: {str(e)}")
        return False

if __name__ == "__main__":
    main()
    