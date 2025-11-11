# Developer Guide

This guide provides detailed instructions for setting up the development environment, building and running the project, and development workflow best practices.

## Table of Contents

- [Environment Setup](#environment-setup)
- [Building and Running](#building-and-running)
- [Development Workflow](#development-workflow)
- [Git Conventions](#git-conventions)
- [Project Structure](#project-structure)
- [Testing](#testing)

## Environment Setup

### Prerequisites

- **Python**: 3.10 or higher
- **Docker**: Latest stable version
- **Docker Compose**: v2.0+
- **Make**: (optional, for convenience commands)
- **Git**: Latest version

### Python Virtual Environment

Create and activate a virtual environment:

**Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Linux/macOS:**
```bash
python -m venv .venv
source .venv/bin/activate
```

### Install Dependencies

**Using pip:**
```bash
pip install -r requirements.txt
```

**Using Poetry (alternative):**
```bash
# Install Poetry
python -m pip install poetry

# Initialize project (if starting fresh)
poetry init --name finance-data-project --author "Your Name" --python "^3.10"

# Install dependencies
poetry install

# Add new packages
poetry add pandas@1.5.3
poetry add kafka-python@2.0.2

# Update packages
poetry update

# Export to requirements.txt
poetry export -f requirements.txt --output requirements.txt --without-hashes
```

### Environment Variables

Create a `.env` file in the project root with the following configuration:

```bash
# Source Code Path
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
MINIO_URL=http://localhost:9000

# Data Paths
METADATA_KEY=/metadata/symbols_metadata.json
BRONZE_PATH=/data/bronze
SILVER_PATH=/data/silver

# Network Configuration
NETWORK_NAME=spark_network

# Spark Worker Configuration
SPARK_IMAGE_VERSION=3.5.3
SPARK_WORKER_MEMORY=2G
SPARK_WORKER_CORES=1
```

**Additional environment files:**

`spark.env`:
```bash
MINIO_ROOT_USER=minio
MINIO_ROOT_PASSWORD=minio123
MINIO_ACCESS_KEY=
MINIO_SECRET_KEY=
MINIO_URL=http://minio:9000

METADATA_KEY=/metadata/symbols_metadata.json
BRONZE_PATH=/dev/data/bronze
SILVER_PATH=/dev/data/silver
```

`airflow.env`:
```bash
MINIO_ROOT_USER=minio
MINIO_ROOT_PASSWORD=minio123
MINIO_ACCESS_KEY=
MINIO_SECRET_KEY=
MINIO_URL=http://minio:9000

METADATA_KEY=/metadata/symbols_metadata.json
BRONZE_PATH=/dev/data/bronze
SILVER_PATH=/dev/data/silver
```

## Building and Running

### Using Make (Recommended)

```bash
# Build Docker images
make build

# Start all services
make up

# Stop all services
make down

# View logs
make logs

# Restart services
make restart
```

### Using Docker Compose Directly

```bash
# Build and start services
docker-compose build
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f

# Restart specific service
docker-compose restart airflow-webserver
```

### Accessing Services

Once services are running, access them at:

| Service | URL | Credentials |
|---------|-----|-------------|
| Airflow Webserver | http://localhost:8081 | user: `airflow`, pass: `airflow` |
| MinIO Console | http://localhost:9001 | user: `minio`, pass: `minio123` |
| Metabase | http://localhost:3000 | Setup on first access |
| Spark Master | http://localhost:8080 | N/A |
| PostgreSQL | localhost:5433 | user: `airflow`, pass: `airflow` |

### Running Pipeline Scripts Locally

[TBD]

## Development Workflow

### Code Organization

- `src/pipeline/extract/` - Data extraction modules
- `src/pipeline/transform/` - Data transformation logic
- `src/pipeline/load/` - Data loading to storage/database
- `src/pipeline/commons/` - Shared utilities and connectors
- `airflow/dags/` - Airflow DAG definitions
- `notebooks/` - Jupyter notebooks for exploration

### Adding New Features

1. Create feature branch: `git checkout -b feat/your-feature-name`
2. Implement changes in appropriate module
3. Add/update tests
4. Run tests locally
5. Commit with conventional commit message
6. Push and create pull request

### Local Testing

Run Python modules directly for quick iteration:

```bash
# Test extraction
python -c "from pipeline.extract.vnstock_lib import VnstockLibExtractor; print('OK')"

# Test connection
python -c "from pipeline.commons.connectors.s3 import S3Connector; print('OK')"
```

### Debugging DAGs

Test Airflow tasks without the scheduler:

```bash
# Test specific task
docker-compose exec airflow-webserver \
  airflow tasks test vnstock_ingest_stock run_test_script_task 2024-01-01
```

## Git Conventions

This project follows [Conventional Commits](https://www.conventionalcommits.org/) specification.

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Commit Types

| Type | Description | Example |
|------|-------------|---------|
| `feat` | A new feature | `feat(pipeline): add company data extraction` |
| `fix` | A bug fix | `fix(airflow): resolve DAG parsing error` |
| `docs` | Documentation only changes | `docs(readme): update setup instructions` |
| `style` | Code style changes (formatting, semicolons, etc.) | `style(pipeline): format with black` |
| `refactor` | Code refactoring without behavior change | `refactor(extract): simplify API calls` |
| `perf` | Performance improvements | `perf(transform): optimize data processing` |
| `test` | Adding or updating tests | `test(extract): add unit tests for extractor` |
| `build` | Build system or dependency changes | `build(deps): upgrade pandas to 2.0` |
| `ci` | CI/CD configuration changes | `ci(github): add workflow for testing` |
| `chore` | Other changes (maintenance) | `chore(gitignore): add venv folder` |
| `revert` | Revert a previous commit | `revert: revert commit abc123` |

### Examples

```bash
# Feature
git commit -m "feat(extract): add VNStock company info extractor"

# Bug fix
git commit -m "fix(dag): correct task dependencies in ingestion DAG"

# Documentation
git commit -m "docs(architecture): add system design diagram"

# Refactoring
git commit -m "refactor(load): extract S3 upload logic to helper"
```

### Branch Naming

- `feat/feature-name` - New features
- `fix/bug-description` - Bug fixes
- `docs/what-changed` - Documentation updates
- `refactor/component-name` - Code refactoring

## Project Structure

```
finance_hub/
├── airflow/              # Airflow orchestration
│   ├── dags/            # DAG definitions
│   │   ├── vnstock_data_ingestion.py
│   │   ├── vnstock_data_ingestion_company.py
│   │   ├── vnstock_transform_stock.py
│   │   └── vnstock_transform_company.py
│   ├── logs/            # Airflow execution logs
│   ├── plugins/         # Custom Airflow plugins
│   └── secrets/         # Connection configurations
├── docs/                # Documentation
│   ├── developer_guide.md
│   ├── architecture.md
│   ├── roadmap.md
│   └── image/          # Screenshots and diagrams
├── minio/               # MinIO data storage
│   └── data/           # Bronze/silver layer data
├── notebooks/           # Jupyter notebooks for analysis
├── postgresql/          # PostgreSQL setup
│   └── init-scripts/   # Database initialization SQL
├── spark/               # Spark configurations
│   ├── jobs/           # Spark job scripts
│   └── Dockerfile      # Custom Spark image
├── src/                 # Source code
│   └── pipeline/       # Pipeline modules
│       ├── extract/    # Data extraction
│       │   ├── base.py
│       │   └── vnstock_lib.py
│       ├── transform/  # Data transformation
│       │   ├── base.py
│       │   └── vnstock.py
│       ├── load/       # Data loading
│       │   ├── base.py
│       │   ├── s3.py
│       │   └── postgres.py
│       └── commons/    # Shared utilities
│           ├── connectors/
│           ├── helpers.py
│           ├── constants.py
│           └── custom_exceptions.py
├── docker-compose.yml   # Service orchestration
├── Makefile            # Build automation
├── pyproject.toml      # Python project config
├── requirements.txt    # Python dependencies
└── README.md           # Project overview
```

## Testing

[TBD]

## Troubleshooting

### Common Issues
[TBD]

## Additional Resources

- [Apache Airflow Documentation](https://airflow.apache.org/docs/)
- [MinIO Documentation](https://min.io/docs/)
- [PySpark Documentation](https://spark.apache.org/docs/latest/api/python/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [VNStock Documentation](https://github.com/thinh-vu/vnstock)