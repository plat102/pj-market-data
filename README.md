# Finance Data

A data project.

```
investment-data-project/
│
├── README.md                   # Project documentation & usage
├── docker-compose.yml          # Docker Compose file to spin up services
├── terraform/                  # Terraform scripts for cloud resources (optional)
│   ├── main.tf                 # Main Terraform configuration
│   └── variables.tf            # Variables used in Terraform setup
│
├── data/                       # Folder for raw and processed data (local runs)
│   ├── raw/                    # Raw API or web scraped data
│   └── processed/              # Processed and transformed data
│
├── ingestion/                  # Data ingestion scripts and API connectors
│   ├── stock_api.py            # Fetch stock data from public API
│   ├── news_api.py             # Fetch news data from news API
│   └── web_scraper.py          # Web scraper for mortgage/accommodation data
│
├── airflow/                    # Airflow DAGs and configurations
│   ├── dags/                   # Folder for Airflow DAGs
│   │   └── stock_pipeline_dag.py # Example DAG for stock data ingestion
│   └── airflow.cfg             # Airflow configuration file
│
├── kafka/                      # Kafka configurations and consumers/producers
│   ├── kafka_producer.py       # Kafka producer for stock data stream
│   ├── kafka_consumer.py       # Kafka consumer to read and process data
│   └── config/                 # Kafka configurations (e.g., topics, brokers)
│
├── spark/                      # Spark batch & streaming jobs
│   ├── batch_job.py            # Spark job for batch ETL
│   ├── streaming_job.py        # Spark job for Kafka streaming processing
│   └── config/                 # Spark configurations (e.g., settings, cluster)
│
├── sql/                        # SQL queries and database scripts
│   ├── create_tables.sql       # SQL script to create tables in PostgreSQL
│   └── queries.sql             # Sample queries to analyze the data
│
├── minio/                      # MinIO configuration files
│   └── buckets/                # Pre-defined bucket names and structure
│
├── monitoring/                 # Monitoring with Prometheus/Grafana
│   ├── prometheus.yml          # Prometheus configuration
│   └── grafana/                # Grafana dashboards and settings
│
├── notebooks/                  # Jupyter notebooks for exploratory analysis
│   └── analysis.ipynb          # Example notebook to explore the data
│
├── requirements.txt            # Python dependencies for ingestion and jobs
├── .env                        # Environment variables (API keys, passwords, etc.)
└── scripts/                    # Utility scripts (e.g., clean data, health checks)
    └── health_check.py         # Script to check the health of all services
```