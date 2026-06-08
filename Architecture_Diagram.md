# Architecture Diagram

## DVD Rental Big Data Management Project

## 1. System Architecture Overview

The project follows a structured data analytics pipeline. The DVD Rental database is restored into PostgreSQL using Docker. Python scripts then connect to the database, validate the tables, perform exploration, create merged datasets, generate business insights, and feed the final outputs into a Streamlit dashboard and executive report.

## 2. Architecture Flow

```text
+-----------------------------+
|     DVD Rental Backup       |
|     dvdrental.tar           |
+-------------+---------------+
              |
              v
+-----------------------------+
| Docker Compose Environment  |
| - PostgreSQL                |
| - pgAdmin                   |
+-------------+---------------+
              |
              v
+-----------------------------+
| PostgreSQL Database         |
| Database: dvdrental         |
| Tables: customer, rental,   |
| payment, film, inventory,   |
| store, category, etc.       |
+-------------+---------------+
              |
              v
+-----------------------------+
| Python Data Pipeline        |
| SQLAlchemy + Pandas         |
+-------------+---------------+
              |
              v
+-----------------------------+
| 1_setup_validate.py         |
| - Connect to database       |
| - List tables               |
| - Validate critical tables  |
| - Count rows                |
| - Check data quality        |
+-------------+---------------+
              |
              v
+-----------------------------+
| 2_data_exploration.py       |
| - Schema inspection         |
| - Missing value checks      |
| - Descriptive statistics    |
| - Outlier checks            |
| - Initial visualizations    |
+-------------+---------------+
              |
              v
+-----------------------------+
| 3_data_relationships.py     |
| - Create merged datasets    |
| - Document join keys        |
| - Validate merged outputs   |
+-------------+---------------+
              |
              v
+-----------------------------+
| 4_analysis.py               |
| - Customer analytics        |
| - Revenue optimization      |
| - Store performance         |
| - Inventory analysis        |
| - Recommendation insights   |
+-------------+---------------+
              |
              v
+-----------------------------+
| Output Folders              |
| - tables/                   |
| - merges/                   |
| - results/                  |
| - exports/                  |
+-------------+---------------+
              |
              v
+-----------------------------+
| 5_dashboard.py              |
| Streamlit Dashboard         |
| - KPI cards                 |
| - Charts                    |
| - Tables                    |
| - Multi-page navigation     |
+-------------+---------------+
              |
              v
+-----------------------------+
| Executive Report            |
| README                      |
| Business Recommendations    |
+-----------------------------+
```

## 3. Main Components

### Docker Compose

Docker Compose is used to run the required services in a consistent environment. The main services are PostgreSQL and pgAdmin.

### PostgreSQL

PostgreSQL stores the restored DVD Rental database. It acts as the main data source for the project.

### pgAdmin

pgAdmin provides a browser-based interface for managing and inspecting the PostgreSQL database.

### Python Scripts

Python is used for database validation, exploratory analysis, data integration, advanced analysis, and dashboard preparation.

### Output Folders

The project saves generated outputs into organized folders:

* `tables/`: validation summaries, descriptive statistics, analysis tables
* `merges/`: merged datasets used for analysis
* `results/`: generated charts and visualizations
* `exports/`: written reports and business summaries

### Streamlit Dashboard

Streamlit presents the final insights in an interactive web dashboard with multiple pages, KPI cards, charts, and summary tables.

## 4. Data Movement Summary

1. The DVD Rental backup file is restored into PostgreSQL.
2. Python connects to PostgreSQL using SQLAlchemy and psycopg2.
3. Validation and exploration scripts inspect the raw database tables.
4. Relationship mapping creates merged analysis-ready datasets.
5. Advanced analysis scripts generate business insights and charts.
6. Streamlit reads the generated CSV files and presents the dashboard.
7. The executive report summarizes the key findings and recommendations.

## 5. Reproducibility

The architecture supports reproducibility because the services are defined in `docker-compose.yml`, credentials are stored in `.env`, dependencies are listed in `requirements.txt`, and the scripts are numbered in the order they should be executed.
