from httpx import get
from pyspark.sql import SparkSession

def main():
    spark = (SparkSession.builder
             .appName("TestJob")
             .getOrCreate())
    
    data = [{'tes1': 1}, {'test2': 2}, {'test3': 3}]
    df = spark.createDataFrame(data, ['name', 'value'])
    df.show()
    
    spark.stop()

if __name__ == "__main__":
    main()
    