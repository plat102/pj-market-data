# Market Data Hub

A data project.

## References

* [Python Poetry in 8 Minutes](https://www.youtube.com/watch?v=Ji2XDxmXSOM&ab_channel=ArjanCodes)

Spark

* [Setting up Apache Airflow and Spark Clusters on Docker](https://www.youtube.com/watch?v=4IaE2eHTfR0&ab_channel=CodeWithYu)
* [Setting up a Spark standalone cluster on Docker in layman terms | by Marin Aglić | Medium](https://medium.com/@MarinAgli1/setting-up-a-spark-standalone-cluster-on-docker-in-layman-terms-8cbdc9fdd14b)

Airflow

* [GitHub - Rafavermar/SparkAirflow-PythonScala](https://github.com/Rafavermar/SparkAirflow-PythonScala)
* [Building the image — docker-stack Documentation](https://airflow.apache.org/docs/docker-stack/build.html#extending-the-image)

## Requirements

### Objectives

1. Unified Data Aggregation
2. Real-time and Batch Data Ingestion
3. Data Lake and Warehouse Storage
4. Pipeline Orchestration & Scheduling

Others:
Analytics & Insights Delivery
Monitoring & Alerting
Scalability & Modularity
Cost-Effective and Free Usage

### Deliverables

**Phase 1: Ingestion** **& Data Collection**

* [X] **Python scripts** to fetch data from APIs (e.g., stock market, news).
* [ ] **Web scraper** (optional) to collect additional data.

**Phase 2: Data Pipelines & Storage**

* [X] Batch pipeline to ingest historical data into the data lake/warehouse.
* [ ] Streaming pipeline using Kafka to handle real-time data.
* [X] Storage setup in **MinIO/S3** for raw and processed data.

**Phase 3: Orchestration & Scheduling**

* [ ] Airflow DAGs to orchestrate and automate the pipelines.
* [ ] Event-driven pipelines triggered by Kafka events.

**Phase 4: Analytics & Insights**

* [ ] SQL queries and Python scripts to extract insights.
* [X] Jupyter notebooks connection for analysis
* [ ] Metabase or Grafana dashboards for visualization.

**Phase 5: Monitoring & Alerts**

* [ ] Prometheus metrics and Grafana dashboards to monitor the system.
* [ ] Alerts configured for pipeline failures or API downtime.

#### Success criteria

* End-to-end pipeline integration: From data ingestion to transformation and analytics
* Scalable and modular architecture: Easy to add new data sources or extend functionality.
* Clean and documented code: Maintainable, well-commented scripts, and clear folder organization.
* Working dashboards or reports: Showcasing insights
* Monitoring and alerts in place: Real-time pipeline and infrastructure health checks

## Architecture

### Technology

### Folder structure

```
data-project-market/
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

## Run the project

### Set up environment

```
# From the root of project folder
python -m venv .venv  # Create a virtual environment named venv
source .venv/bin/activate  # Activate it on Linux/macOS
.\.venv\Scripts\activate   # Activate it on Windows
```

#### Sample .env file

.env:

```
SRC_PATH=D:\CODE\de_projects\finance_hub\src

# PostgreSQL Configuration
POSTGRES_USER=airflow
POSTGRES_PASSWORD=airflow
POSTGRES_DB=airflow

# Airflow Paths
AIRFLOW_DAGS=./airflow/dags
AIRFLOW_LOGS=./airflow/logs
AIRFLOW_PLUGINS=./airflow/plugins
AIRFLOW_SECRETS=./airflow/secrets
AIRFLOW_PYTHONPATH=./src
AIRFLOW_DATA=./airflow/data

# Airflow User Configuration
AIRFLOW_UID=50000
AIRFLOW_GID=50000
AIRFLOW_WWW_USER=airflow
AIRFLOW_WWW_PASSWORD=airflow

# MinIO Credentials
MINIO_ROOT_USER=minio
MINIO_ROOT_PASSWORD=minio123
MINIO_ACCESS_KEY=
MINIO_SECRET_KEY=
MINIO_URL= http://localhost:9000

METADATA_KEY="/metadata/symbols_metadata.json"
BRONZE_PATH="/data/bronze"
SILVER_PATH="/data/silver"

# Network Configuration
NETWORK_NAME=spark_network

# Spark Worker Configuration
SPARK_IMAGE_VERSION=3.5.3
SPARK_WORKER_MEMORY=2G
SPARK_WORKER_CORES=1

```

spark.env

```
# MinIO Credentials
MINIO_ROOT_USER=minio
MINIO_ROOT_PASSWORD=minio123
MINIO_ACCESS_KEY=
MINIO_SECRET_KEY=
MINIO_URL= http://minio:9000

METADATA_KEY="/metadata/symbols_metadata.json"
BRONZE_PATH="/dev/data/bronze"
SILVER_PATH="/dev/data/silver"
```

Airflow.env

```
# MinIO Credentials
MINIO_ROOT_USER=minio
MINIO_ROOT_PASSWORD=minio123
MINIO_ACCESS_KEY=
MINIO_SECRET_KEY=
MINIO_URL= http://minio:9000

METADATA_KEY="/metadata/symbols_metadata.json"
BRONZE_PATH="/dev/data/bronze"
SILVER_PATH="/dev/data/silver"

```

#### `poettry` for Dependency Management

* [Python Poetry in 8 Minutes](https://www.youtube.com/watch?v=Ji2XDxmXSOM&ab_channel=ArjanCodes)

```
python -m pip install poetry
poetry init --name finance-data-project --author "Thu Phan" --python "^3.10"
```

Install packages

```
poetry add pandas@1.5.3  # Installs pandas 1.5.3
poetry add kafka-python@2.0.2
```

Update package

```
poetry update panda

# update all
poetry update
```

Generate requirements.txt if needed

```
poetry export -f requirements.txt --output requirements.txt --without-hashes
```

### Build and run

```
make build
make up
```

![1729573391650](image/README/1729573391650.png)

### Accessing services

| Service                    | URL                                         | Port |
| -------------------------- | ------------------------------------------- | ---- |
| Airflow Webserver          | [http://localhost:8080](http://localhost:8080) | 8080 |
| MinIO Console              | [http://localhost:9001](http://localhost:9001) | 9001 |
| Spark Master               | [http://localhost:8080](http://localhost:8080) | 8080 |
| Spark notebook application | [http://localhost:4040](http://localhost:4040) |      |
| PostgreSQL                 | N/A                                         | 5433 |

- Ensure that the services are running before attempting to access the URLs.
- Use the provided access and secret keys (in `docker-compose.yaml`) to log in.

#### Airflow

DAGs:

##### Run the ingestion pipeline(s)

![1733458317452](image/README/1733458317452.png)

##### Run the transform pipeline()s)

![1734772521444](image/README/1734772521444.png)

#### MinIO

![1733458515605](image/README/1733458515605.png)

#### Spark Notebooks

#### Spark UI

#### Metabase

## Notes:

#### git convention

[Conventional Commits Cheatsheet (github.com)](https://gist.github.com/qoomon/5dfcdf8eec66a051ecd85625518cfd13)

| Type     | Description                                                                                                 |
| -------- | ----------------------------------------------------------------------------------------------------------- |
| feat     | A new feature                                                                                               |
| fix      | A bug fix                                                                                                   |
| docs     | Documentation only changes                                                                                  |
| style    | Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc.)     |
| refactor | A code change that neither fixes a bug nor adds a feature                                                   |
| perf     | A code change that improves performance                                                                     |
| test     | Adding missing tests or correcting existing tests                                                           |
| build    | Changes that affect the build system or external dependencies (example scopes: gulp, broccoli, npm)         |
| ci       | Changes to our CI configuration files and scripts (example scopes: Travis, Circle, BrowserStack, SauceLabs) |
| chore    | Other changes that don't modify `src` or `test` files                                                   |
| revert   | Reverts a previous commit                                                                                   |

---

## Contact me
