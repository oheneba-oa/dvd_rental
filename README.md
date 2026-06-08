# DVD Rental Big Data Management Project

## 1. Project Overview

This project is an industry-based analytics project  which uses the PostgreSQL DVD Rental database to analyse customer behaviour, revenue performance, inventory usage, store performance, and recommendation opportunities.

The objective is to build a complete analytics workflow that covers database setup, validation, exploratory data analysis, data integration, advanced business analysis, dashboard development, and executive reporting.

The project was developed using Docker, PostgreSQL, Python, Pandas, SQLAlchemy, Matplotlib, Seaborn, and Streamlit.

---

## 2. Project Structure

```text
Big_Data_Management_Project/
│
├── .env
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
│
├── 1_setup_validate.py
├── 2_data_exploration.py
├── 3_data_relationships.py
├── 4_analysis.py
├── 5_dashboard.py
│
├── Executive_Report.md
├── README.md
│
├── data/
│   ├── backups/
│   ├── postgres/
│   ├── pgadmin/
│   └── uploads/
│
├── exports/
├── tables/
├── merges/
└── results/
```

---

## 3. Tools and Libraries Used

### Main Tools

* Docker
* Docker Compose
* PostgreSQL
* pgAdmin
* Python 3.11
* Streamlit

### Python Libraries

* pandas
* sqlalchemy
* psycopg2-binary
* python-dotenv
* matplotlib
* seaborn
* streamlit
* scikit-learn
* plotly

---

## 4. Environment Variables

The project uses a `.env` file to store database and pgAdmin connection details.

```env
POSTGRES_USER=student
POSTGRES_PASSWORD=student
POSTGRES_DB=dvdrental
POSTGRES_PORT=5432

PGADMIN_EMAIL=admin@admin.com
PGADMIN_PASSWORD=admin
PGADMIN_PORT=8080
```

---

## 5. Docker Setup

The project uses Docker Compose to run PostgreSQL and pgAdmin.

To start the services, run:

```bash
docker compose up -d
```

To check if the containers are running, run:

```bash
docker ps
```

Expected containers:

```text
bdm_postgres
bdm_pgadmin
```

pgAdmin can be opened in the browser using:

```text
http://localhost:8080
```

Login details:

```text
Email: admin@admin.com
Password: admin
```

---

## 6. PostgreSQL and pgAdmin Connection

In pgAdmin, register the PostgreSQL server using the following details:

```text
Name: BDM Postgres
Host name/address: postgres
Port: 5432
Maintenance database: dvdrental
Username: student
Password: student
```

The host is `postgres` inside pgAdmin because both pgAdmin and PostgreSQL are running inside Docker Compose.

For Python scripts running from the local computer, the database host is:

```text
localhost
```

---

## 7. Database Restoration

The DVD Rental database was restored into PostgreSQL under the database name:

```text
dvdrental
```

The backup file should be placed in:

```text
data/backups/dvdrental.tar
```

Inside pgAdmin, the restore path is:

```text
/backups/dvdrental.tar
```

After restoring the database, the following key tables should be available:

```text
actor
address
category
city
country
customer
film
film_actor
film_category
inventory
language
payment
rental
staff
store
```

---

## 8. Installing Python Requirements

Install the required Python libraries using:

```bash
python -m pip install -r requirements.txt
```

If `psycopg2` is missing, install it directly using:

```bash
python -m pip install psycopg2-binary
```

---

## 9. How to Run the Project

Run the scripts in the following order.

### Step 1: Database Validation

```bash
python 1_setup_validate.py
```

This script connects to PostgreSQL, lists available tables, validates critical DVD Rental tables, counts rows, checks basic data quality issues, and exports validation outputs.

Main outputs:

```text
exports/database_validation_report.txt
tables/table_row_counts.csv
tables/data_quality_summary.csv
```

---

### Step 2: Exploratory Data Analysis

```bash
python 2_data_exploration.py
```

This script inspects schemas, checks missing values, produces descriptive statistics, identifies outliers, and creates initial visualizations.

Main outputs:

```text
tables/schema_summary.csv
tables/missing_values_summary.csv
tables/descriptive_statistics.csv
tables/outlier_summary.csv

results/monthly_revenue.png
results/top_film_categories_by_revenue.png
results/top_customers_by_revenue.png
results/rentals_by_store.png
```

---

### Step 3: Data Relationship Mapping

```bash
python 3_data_relationships.py
```

This script creates merged datasets for customer revenue, film category revenue, store performance, and inventory turnover.

Main outputs:

```text
merges/customer_revenue_dataset.csv
merges/film_category_revenue_dataset.csv
merges/store_performance_dataset.csv
merges/inventory_turnover_dataset.csv
exports/data_relationships_report.txt
```

---

### Step 4: Advanced Business Analysis

```bash
python 4_analysis.py
```

This script performs customer segmentation, churn risk analysis, revenue optimization, store performance analysis, slow-moving inventory analysis, and recommendation candidate analysis.

Main outputs:

```text
tables/customer_segments.csv
tables/churn_risk_customers.csv
tables/revenue_by_category.csv
tables/pricing_insight.csv
tables/store_performance_analysis.csv
tables/slow_moving_inventory.csv
tables/recommendation_candidates.csv

exports/business_insights_summary.txt

results/customer_segments.png
results/churn_risk_customers.png
results/revenue_by_category_analysis.png
results/store_revenue_comparison.png
results/slow_moving_inventory.png
results/recommendation_categories.png
```

---

### Step 5: Streamlit Dashboard

```bash
streamlit run 5_dashboard.py
```

The dashboard opens in the browser, usually at:

```text
http://localhost:8501
```

The dashboard includes:

* Executive overview
* Customer analytics
* Revenue optimization
* Inventory and operations
* Recommendation insights
* KPI cards
* Charts and summary tables
* Multi-page sidebar navigation

---

## 10. Analytical Areas Covered

The project covers four main analytical themes.

### Customer Analytics

* Customer value segmentation
* Customer revenue contribution
* Average payment behaviour
* Churn risk based on payment recency

### Revenue Optimization

* Revenue by film category
* Rental volume by category
* Average payment by category
* Pricing-related insights

### Inventory and Operations

* Store-level revenue comparison
* Customer and inventory comparison by store
* Revenue per inventory item
* Rentals per inventory item
* Slow-moving inventory identification

### Innovation or Custom Analysis

* Simple category-based recommendation strategy
* High-priority recommendation categories
* Promotional targeting based on strong revenue categories

---

## 11. Key Findings Summary

The analysis showed that the high-value customer segment generated 26,009.63 in revenue, compared with 15,329.62 from the low-value segment. Sports was the strongest film category, generating 4,892.19 from 1,179 rentals. Music was the lowest revenue category, generating 3,071.52 from 830 rentals.

Store performance was balanced. Store 1 generated 30,628.91 in revenue, while Store 2 generated 30,683.13. Store 1 had more customers, but Store 2 generated slightly higher total revenue.

The slow-moving inventory analysis identified film copies with very low rental counts, including one item with zero rentals and zero revenue.

---

## 12. Main Recommendations

1. Protect high-value customers through loyalty offers and personalized promotions.
2. Increase engagement among active customers to improve repeat rentals.
3. Promote high-performing categories such as Sports, Sci-Fi, Animation, Drama, and Comedy.
4. Review low-performing categories such as Music, Travel, Children, Classics, and Horror.
5. Monitor slow-moving inventory and reduce or promote underused stock.
6. Improve store-level stock allocation based on revenue and rental efficiency.
7. Start with a simple category-based recommendation approach before moving to advanced modelling.

---

## 13. Ethical Considerations and Limitations

The dataset contains customer-related information, including names and emails. In a real business environment, such information should be handled responsibly and should not be exposed unnecessarily in public dashboards or reports.

The analysis is based on historical transaction data and does not include external factors such as competitor activity, customer satisfaction, marketing campaigns, or streaming service trends. Churn risk was estimated using payment recency, not direct customer feedback. The recommendation model is simple and category-based, so future improvements could include customer-level behavioural modelling.

---

## 14. Notes on Reproducibility

The project is reproducible because:

* Database credentials are stored in `.env`
* Services are managed using Docker Compose
* Python dependencies are listed in `requirements.txt`
* Scripts are numbered and should be run in order
* Outputs are saved into clearly named folders
* The dashboard reads from generated analysis outputs
* Reports document assumptions, joins, limitations, and business recommendations

---

## 15. Author

Name: Oheneba Oduro-Asare
