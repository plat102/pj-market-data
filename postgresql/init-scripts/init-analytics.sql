-- Create a new database for analytics
CREATE DATABASE analytics;

-- Connect to the analytics database
\c analytics

-- Create schemas
CREATE SCHEMA IF NOT EXISTS staging AUTHORIZATION airflow;
CREATE SCHEMA IF NOT EXISTS intermediate AUTHORIZATION airflow;
CREATE SCHEMA IF NOT EXISTS mart AUTHORIZATION airflow;

-- Create a user for dbt
CREATE USER dbt_user WITH PASSWORD 'dbt_password';

-- Create a user for Metabase
CREATE USER metabase_user WITH PASSWORD 'metabase_password';

-- Grant permissions to dbt_user for all schemas
GRANT CONNECT ON DATABASE analytics TO dbt_user;
GRANT USAGE ON SCHEMA staging TO dbt_user;
GRANT USAGE ON SCHEMA intermediate TO dbt_user;
GRANT USAGE ON SCHEMA mart TO dbt_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA staging TO dbt_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA intermediate TO dbt_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA mart TO dbt_user;

-- Set default privileges for dbt_user
ALTER DEFAULT PRIVILEGES IN SCHEMA staging
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO dbt_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA intermediate
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO dbt_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA mart
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO dbt_user;

-- Grant permissions to metabase_user for intermediate and mart schemas
GRANT CONNECT ON DATABASE analytics TO metabase_user;
GRANT USAGE ON SCHEMA intermediate TO metabase_user;
GRANT USAGE ON SCHEMA mart TO metabase_user;
GRANT SELECT ON ALL TABLES IN SCHEMA intermediate TO metabase_user;
GRANT SELECT ON ALL TABLES IN SCHEMA mart TO metabase_user;

-- Set default privileges for metabase_user
ALTER DEFAULT PRIVILEGES IN SCHEMA intermediate
GRANT SELECT ON TABLES TO metabase_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA mart
GRANT SELECT ON TABLES TO metabase_user;
