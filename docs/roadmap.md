# Project Roadmap

## Objectives

Build a production-ready data engineering solution for Vietnamese stock market analysis:

1. **Batch Data Pipeline**: Extract, transform, and load stock market data from VNStock API
2. **Modern Data Stack**: Airflow orchestration, Spark processing, MinIO data lake, PostgreSQL warehouse
3. **Analytics & Visualization**: Enable business intelligence through Metabase dashboards
4. **Best Practices**: Modular code, medallion architecture, containerized deployment
5. **Production Patterns**: Error handling, logging, configuration management, data quality

## Success Criteria

- ✅ End-to-end batch pipeline from API to data warehouse
- ✅ Scheduled DAGs running reliably in Airflow
- ✅ Data stored in organized bronze/silver layers (data lake)
- ✅ PySpark transformations for data cleaning and standardization
- ✅ Structured data loaded to PostgreSQL for analytics
- ✅ Metabase dashboards for business intelligence
- ✅ Jupyter notebooks for ad-hoc analysis and exploration
- ✅ Docker-compose deployment for full stack reproducibility
- ✅ Comprehensive documentation for setup and usage

## Scope

### In Scope (Implemented)

**Data Ingestion**

- VNStock API integration (stock prices, company info)
- Batch extraction with error handling
- Historical data retrieval

**Data Storage**

- MinIO data lake (S3-compatible)
- Medallion architecture (bronze/silver layers)
- PostgreSQL data warehouse for analytical data
- PostgreSQL databases for Airflow and Metabase metadata

**Processing & Orchestration**

- Apache Airflow DAGs for scheduling
- PySpark transformations
- Data validation and cleaning
- PostgreSQL loaders for structured data

**Infrastructure**

- Docker Compose multi-service setup
- Makefile build automation
- Environment configuration
- Service networking and orchestration

**Analytics & Visualization**

- Metabase for business intelligence dashboards
- PostgreSQL as data source for reporting
- Jupyter notebooks for ad-hoc exploration
- SQL query interface for analysts

### Out of Scope (Not Implemented)

- Real-time streaming (Kafka)
- Comprehensive monitoring stack (Prometheus/Grafana)
- ML model training and deployment
- Cloud deployment (AWS/Azure)
- Advanced data quality framework
- Automated testing (CI/CD pipelines)

## Specification

### Data Sources

- **VNStock API**: Vietnamese stock market data (prices, company information)
- **Update Frequency**: Daily batch ingestion
- **Coverage**: All stocks listed on HOSE, HNX, UPCOM exchanges

### Data Architecture

- **Bronze Layer**: Raw JSON data from API
- **Silver Layer**: Cleaned, validated Parquet files
- **Gold Layer**: (Future) Aggregated business metrics

### Pipeline Components

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Extraction | Python + VNStock | API data retrieval |
| Data Lake | MinIO | S3-compatible object storage |
| Processing | PySpark | Data transformation |
| Orchestration | Airflow | Workflow scheduling |
| Data Warehouse | PostgreSQL | Structured analytical data |
| Visualization | Metabase | BI dashboards and reports |
| Analysis | Jupyter | Ad-hoc exploration |

### Key DAGs

1. **vnstock_ingest_stock**: Daily stock price ingestion
2. **vnstock_ingest_company**: Company information updates
3. **vnstock_transform_stock**: Bronze to silver transformations
4. **vnstock_transform_company**: Company data processing

### Performance Requirements

- Ingest ~2000 stocks daily
- Transform within 30 minutes
- Store 1+ year of historical data
- Support ad-hoc analysis queries

## Future Enhancements

Tracked in project management tools (Notion/Jira):

- **Testing**: Unit and integration test coverage
- **Monitoring**: Custom metrics and alerting
- **Data Quality**: Validation framework
- **Gold Layer**: Business-ready aggregations
- **Streaming**: Real-time price updates (Kafka)
- **ML**: Predictive models and feature engineering
- **Cloud**: AWS/Azure deployment

---

**Last Updated**: November 2025
**Status**: Active Development
