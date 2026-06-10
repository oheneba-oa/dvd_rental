"""
1_setup_validate.py

Purpose:
This script connects to the PostgreSQL DVD Rental database,
lists available base tables, checks important tables, counts rows,
and performs basic data quality checks.

Outputs:
- exports/database_validation_report.txt
- tables/table_row_counts.csv
- tables/data_quality_summary.csv
"""

import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv


# ------------------------------------------------------------
# 1. Load database details from the .env file
# ------------------------------------------------------------
load_dotenv()

DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_NAME = os.getenv("POSTGRES_DB")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")

# The Python scripts run on the local machine, so localhost is used
# to connect to the PostgreSQL container through the exposed port.
DB_HOST = "localhost"


# ------------------------------------------------------------
# 2. Create database connection
# ------------------------------------------------------------
connection_url = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(connection_url)


# ------------------------------------------------------------
# 3. Define important tables expected in the DVD Rental database
# ------------------------------------------------------------
critical_tables = [
    "actor",
    "address",
    "category",
    "city",
    "country",
    "customer",
    "film",
    "film_actor",
    "film_category",
    "inventory",
    "language",
    "payment",
    "rental",
    "staff",
    "store",
]


# ------------------------------------------------------------
# 4. Create output folders if they do not exist
# ------------------------------------------------------------
os.makedirs("exports", exist_ok=True)
os.makedirs("tables", exist_ok=True)


# ------------------------------------------------------------
# 5. Connect and validate database
# ------------------------------------------------------------

# A try-except block is used so that connection or query errors
# are displayed clearly instead of stopping the script without context.
try:
    with engine.connect() as connection:
        print("Database connection successful.")

        # Get only real/base tables from the public schema.
        # This avoids PostgreSQL views such as actor_info and film_list.
        tables_query = """
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
        AND table_type = 'BASE TABLE'
        ORDER BY table_name;
        """

        available_tables_df = pd.read_sql(tables_query, connection)
        available_tables = available_tables_df["table_name"].tolist()

        print("\nAvailable tables:")
        print(available_tables)

        # Check whether all important tables exist
        missing_tables = [
            table for table in critical_tables
            if table not in available_tables
        ]

        if missing_tables:
            print("\nMissing critical tables:")
            print(missing_tables)
        else:
            print("\nAll critical tables are present.")

        # ------------------------------------------------------------
        # 6. Count rows in each table
        # ------------------------------------------------------------
        row_counts = []

        for table in available_tables:
            count_query = text(f'SELECT COUNT(*) AS row_count FROM "{table}";')
            result = connection.execute(count_query).fetchone()

            row_counts.append({
                "table_name": table,
                "row_count": result[0]
            })

        row_counts_df = pd.DataFrame(row_counts)
        row_counts_df.to_csv("tables/table_row_counts.csv", index=False)

        print("\nRow counts saved to tables/table_row_counts.csv")

        # ------------------------------------------------------------
        # 7. Basic data quality checks
        # ------------------------------------------------------------
        quality_results = []

        for table in available_tables:
            sample_df = pd.read_sql(
                f'SELECT * FROM "{table}" LIMIT 1000;',
                connection
            )

            total_rows = row_counts_df.loc[
                row_counts_df["table_name"] == table,
                "row_count"
            ].values[0]

            # Count missing values in the sample
            missing_values = sample_df.isnull().sum().sum()

            # Some DVD Rental columns contain PostgreSQL arrays/lists,
            # for example special_features in the film table.
            # Pandas cannot check duplicates when list values are present,
            # so list values are converted to strings only for this check.
            sample_for_duplicates = sample_df.copy()

            for column in sample_for_duplicates.columns:
                sample_for_duplicates[column] = sample_for_duplicates[column].apply(
                    lambda value: str(value) if isinstance(value, list) else value
                )

            duplicate_rows = sample_for_duplicates.duplicated().sum()

            quality_results.append({
                "table_name": table,
                "total_rows": total_rows,
                "sample_rows_checked": len(sample_df),
                "missing_values_in_sample": missing_values,
                "duplicate_rows_in_sample": duplicate_rows
            })

        quality_df = pd.DataFrame(quality_results)
        quality_df.to_csv("tables/data_quality_summary.csv", index=False)

        print("Data quality summary saved to tables/data_quality_summary.csv")

        # ------------------------------------------------------------
        # 8. Write validation report
        # ------------------------------------------------------------
        report = f"""
DATABASE VALIDATION REPORT
==========================

Database Name: {DB_NAME}
Database Host: {DB_HOST}
Database Port: {DB_PORT}

Connection Status:
Successful

Number of Base Tables Found:
{len(available_tables)}

Available Base Tables:
{", ".join(available_tables)}

Critical Tables Checked:
{", ".join(critical_tables)}

Missing Critical Tables:
{", ".join(missing_tables) if missing_tables else "None"}

Row Count Output:
tables/table_row_counts.csv

Data Quality Output:
tables/data_quality_summary.csv

Summary:
The PostgreSQL connection was successful. The DVD Rental database was inspected,
critical base tables were validated, row counts were generated, and basic data
quality checks were performed using sample records from each table.

Note:
Only base tables were selected for validation. Database views such as actor_info,
film_list, customer_list, sales_by_store, and sales_by_film_category were excluded
from this setup validation stage.
"""

        with open(
            "exports/database_validation_report.txt",
            "w",
            encoding="utf-8"
        ) as file:
            file.write(report)

        print("Validation report saved to exports/database_validation_report.txt")

except Exception as error:
    print("Database validation failed.")
    print("Error:", error)